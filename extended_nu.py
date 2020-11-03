from main import interpolation


def Miheev_in(self):
    """Calculates Nusselt number using Miheev's formula"""
    if self.re < 2300:
        return 0.15 * (self.re ** 0.33) * (self.pr_domain ** 0.43) * \
               self.solve_epsilon_t_count() * self.solve_epsilon_l_lam_count()
    elif 2300 <= self.re <= 10_000:
        _re = self.re / 1000
        k_correction = [[2.3, 3.3], [2.4, 3.8], [2.5, 4.4], [3.0, 6.0],
                        [4.0, 10.3], [5.0, 15.5], [6.0, 19.5], [8.0, 27],
                        [10.0, 33.3]]
        for j in range(len(k_correction)):
            if k_correction[j - 1][0] <= _re < k_correction[j][0]:
                return (interpolation(
                    k_correction[j][1], k_correction[j - 1][1],
                    k_correction[j][0], k_correction[j - 1][0], _re)) * \
                       (self.pr_domain ** 0.43) * self.solve_epsilon_t_count()

    else:
        return 0.021 * (self.re ** 0.8) * (self.pr_domain ** 0.43) * \
               self.solve_epsilon_t_count() * \
               self.solve_epsilon_l_turbulent_count()
