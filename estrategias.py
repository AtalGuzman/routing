import abc

class SolucionStrategyAbstract(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def solve(self):
        """Requiere implementarse"""


class SA(SolucionStrategyAbstract):
    def solve(self, problema):
        #TO DO: implementar la resolución según SA y otra técnica
        print("Resolviendo ...")