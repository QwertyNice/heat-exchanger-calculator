from exceptions import InputError, CustomError


class InputValues:
    """Class for reading input data for calculation

    The class takes user input in, which is the start point for the 
    calculation. It contains the attributes required for calculating 
    and selecting a heat exchanger, which are listed below.

    Attributes
    ----------
    matter_heat : str
        The matter of heat domain. The matter can be 'water'.
    matter_cool : str
        The matter of cool domain. The matter can be as in 
        `matter_heat`.
    space_heat : str
        Contains information about the heat domain's flowing space.
        It can be 'in' (tube-side) or 'out' (shell-side). Takes an 
        opposite value of the `space_cool`.
    space_cool : str
        Contains information about the heat domain's flowing space.
        It can be 'in' (tube-side) or 'out' (shell-side). Takes an 
        opposite value of the `space_heat`.
    t_enter_heat : float
        The inlet temperature of the heat domain. Must be more and 
        equal than `t_exit_heat`.
    t_exit_heat : float
        The otlet temperature of the heat domain. Must be less and 
        equal than `t_enter_heat`.
    t_enter_cool : float
        The inlet temperature of the cool domain. Must be less and 
        equal than `t_exit_cool`.
    t_exit_cool : float
        The otlet temperature of the cool domain. Must be more and 
        equal than `t_enter_cool`.

    """
    
    def __init__(self):
        """Each attribute in the __init__ method runs the corresponding 
        private function to receive user input.
        
        """
        
        self.matter_heat = self._input_matter(state='heat')
        self.matter_cool = self._input_matter(state='cool')
        self.space_heat, self.space_cool = self._input_space()

        self.t_enter_heat = self._input_t(point='inlet', state='heat')
        self.t_exit_heat = self._input_t(point='outlet', state='heat')
        self.t_enter_cool = self._input_t(point='inlet', state='cool')
        self.t_exit_cool = self._input_t(point='outlet', state='cool')



    @staticmethod
    def _input_matter(state):
        """Connects a domain's state with its matter."""
        available_matters = {'water'}
        print(f'Avaliable {state} domains: ', end='')
        print(*available_matters, sep=', ', end='.\n')

        matter = input('Enter the type of domain from the list above: ').lower()
        if matter not in available_matters:
            message = 'Incorrect name of the heat domain has been entered, ' \
                      'or it is not in the list of available heat carriers.'
            raise InputError(message)
        print('-' * 69)
        return matter

    @staticmethod
    def _input_space():
        """Connects the domain with its flowing space."""
        space = input('Where does the heat domain flow: \'in\' (tube-side) or' \
                      ' \'out\' (shell-side)? ').lower()
        if space not in ('in', 'out'):
            message = 'Incorrect flowing space has been entered.'
            raise InputError(message)
        print('-' * 69)

        if space == 'in':
            return 'in', 'out'
        return 'out', 'in'

    @staticmethod
    def _input_t(point, state):
        """Connects the domain with its inlet/outlet temperature."""
        t = input(f'Enter the {point} temperature of the {state} domain, °C: ')
        try:
            t = float(t)
        except ValueError:
            message = f'Incorrect {point} temperature of the {state} domain ' \
                      f'has been entered: {t}'
            raise InputError(message)
        if t < 0:
            message = f'Non-positive {point} temperature of the {state} domain ' \
                      f'has been entered.'
            raise InputError(message)
        print('-' * 69)
        return t
