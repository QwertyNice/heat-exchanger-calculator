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
        The inlet temperature of the heat domain. Must be greater 
        than `t_exit_heat`.
    t_exit_heat : float
        The otlet temperature of the heat domain. Must be less than 
        `t_enter_heat`.
    t_enter_cool : float
        The inlet temperature of the cool domain. Must be less than 
        `t_exit_cool`.
    t_exit_cool : float
        The otlet temperature of the cool domain. Must be greater 
        than `t_enter_cool`.

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
        self._check_value_t()
        
        self.consumption_heat, self.consumption_cool = self._input_consumption()

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
            message = f'Negative {point} temperature of the {state} domain ' \
                      f'has been entered.'
            raise InputError(message)
        print('-' * 69)
        return t

    def _check_value_t(self):
        """Checks the correct dependences between all temperatures"""
        max_t = {'water': 370}
        max_liq_heat_t = max_t[self.matter_heat]
        max_liq_cool_t = max_t[self.matter_cool]
        if self.t_enter_heat <= self.t_exit_heat:
            message = 'Inlet temperature of the heat domain is less than or ' \
                      'equal to the outlet temperature.'
            raise InputError(message)
        if self.t_enter_cool >= self.t_exit_cool:
            message = 'Inlet temperature of the cool domain is greater than or ' \
                      'equal to the outlet temperature.'
            raise InputError(message)
        if not 0 <= (self.t_enter_heat + self.t_exit_heat) / 2 < max_liq_heat_t:
            message = 'Mean temperature of the heat domain goes beyond 0..370°C'
            raise InputError(message)
        if not 0 <= (self.t_enter_cool + self.t_exit_cool) / 2 < max_liq_cool_t:
            message = 'Mean temperature of the cool domain goes beyond 0..370°C'
            raise InputError(message)

    def _input_consumption(self):
        state = input('Enter for which domain the consumption is known: ' \
                      '\'heat\' or \'cool\'? ').lower()
        if state not in ('heat', 'cool'):
            message = 'Incorrect state of domain has been entered.'
            raise InputError(message)
        print('-' * 69)

        consumption = input(f'Enter the consumption of the {state} domain, kg/s' \
                             ' (kilogram per second): ')
        try:
            consumption = float(consumption)
        except ValueError:
            message = f'Incorrect consumption of the {state} domain has been ' \
                      f'entered: {consumption} kg/s.'
            raise InputError(message)
        if consumption <= 0:
            message = f'Non-positive value of the consumption has been entered:' \
                      f' {consumption} kg/s.'
        if state == 'heat':
            return consumption, None
        return None, consumption