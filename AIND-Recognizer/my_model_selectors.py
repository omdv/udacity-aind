import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from sklearn.metrics import log_loss
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """
    
    # Reference: https://discussions.udacity.com/t/understanding-better-model-selection/232987/8
    # n^2 + 2*d*n - 1
    # this parameter growth very quickly with n_states, so the best n_states in my case is almost always stays at min
    def calc_free_params(self, n_states, n_features):
        return n_states*n_states + 2*n_features*n_states - 1

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on BIC scores
        # initiate result
        result = []

        # cycle over a number of components
        for n_states in range(self.min_n_components, self.max_n_components+1):
            try:
                _m = self.base_model(n_states)
                log_like = _m.score(self.X, self.lengths)
                n_samples, n_features = self.X.shape
                BIC = -2. * log_like + self.calc_free_params(n_states, n_features) * np.log(n_samples)
                result.append((BIC, _m))
            except:
                pass
            
        # Find the best model - LOWER BIC is better
        best_model = min(result, key=lambda x: x[0])[1] if result else None

        return best_model

    
class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    https://pdfs.semanticscholar.org/ed3d/7c4a5f607201f3848d4c02dd9ba17c791fc2.pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def select(self):
        # sort out words
        other_words = [self.hwords[_w] for _w in self.words if _w != self.this_word]

        # cycle over a number of states - train current word
        single_model_results = dict()
        for _n in range(self.min_n_components, self.max_n_components+1):
            try:
                _m = self.base_model(_n)
                single_model_results[_n] = (_m.score(self.X, self.lengths), _m)
            except:
                pass
            
        
        # calculate DIC - log_like of current minus all others
        # higher is better
        max_DIC = np.float("-inf")
        best_model = None
        
        for _n in single_model_results:
            _other_scores = [single_model_results[_n][1].score(_w[0], _w[1]) for _w in other_words]
            _DIC = single_model_results[_n][0] - np.mean(_other_scores)
            if _DIC > max_DIC:
                max_DIC = _DIC
                best_model = single_model_results[_n][1]
                
        return best_model



class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        
        # TODO implement model selection using CV
        # The higher log_likelihood is better

        if len(self.sequences) < 3:
            k_folds = len(self.sequences)
        elif len(self.sequences) > 5:
            k_folds = 5
        else:
            k_folds = 3

        # print("{}, seq={}, folds={}".format(self.this_word, len(self.sequences), k_folds))

        # cycle over a number of components
        if k_folds >= 2:
            split_method = KFold(k_folds)
            result = []
            for n_components in range(self.min_n_components, self.max_n_components+1):
                # cycle over folds
                log_likes = []

                if k_folds > 2:
                    for cv_train_idx, cv_test_idx in split_method.split(self.sequences):
                        X_train, L_train = combine_sequences(cv_train_idx, self.sequences)
                        X_test, L_test = combine_sequences(cv_test_idx, self.sequences)
                        try:
                            hmm_model = GaussianHMM(n_components=n_components, covariance_type="diag", n_iter=1000,
                                                random_state=self.random_state, verbose=False).fit(X_train, L_train)
                            log_like = hmm_model.score(X_test, L_test)
                        except:
                            pass

                        # archive scores for averaging
                        log_likes.append(log_like)

                result.append((np.mean(log_likes), n_components))
        
            # find best model - HIGHER log-likelihood the better
            n_components = max(result, key=lambda x: x[0])[1]
            
        # fallback to BIC if not enough data
        elif k_folds < 2:
            classBIC = SelectorBIC(self.words, self.hwords, self.this_word, max_n_components=15)
            return classBIC.select()
            
        return self.base_model(n_components)
