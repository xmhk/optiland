from optiland.optimization.variable.base import VariableBehavior


class AsphereCoeffVariable(VariableBehavior):
    """
    Represents a variable for an aspheric coefficient in an optical system.

    Args:
        optic (Optic): The optic object associated with the variable.
        surface_number (int): The index of the surface in the optical system.
        coeff_number (int): The index of the aspheric coefficient.
        apply_scaling (bool): Whether to apply scaling to the variable.
            Defaults to True.
        **kwargs: Additional keyword arguments.

    Attributes:
        coeff_number (int): The index of the aspheric coefficient.
    """

    def __init__(self, optic, surface_number, coeff_number, apply_scaling=True,
                 **kwargs):
        super().__init__(optic, surface_number, apply_scaling, **kwargs)
        self.coeff_number = coeff_number

    def get_value(self):
        """
        Get the current value of the aspheric coefficient.

        Returns:
            float: The current value of the aspheric coefficient.
        """
        surf = self._surfaces.surfaces[self.surface_number]
        value = surf.geometry.c[self.coeff_number]
        if self.apply_scaling:
            return self.scale(value)
        return value

    def update_value(self, new_value):
        """
        Update the value of the aspheric coefficient.

        Args:
            new_value (float): The new value of the aspheric coefficient.
        """
        if self.apply_scaling:
            new_value = self.inverse_scale(new_value)
        self.optic.set_asphere_coeff(new_value, self.surface_number,
                                     self.coeff_number)

    def scale(self, value):
        """
        Scale the value of the variable for improved optimization performance.

        Args:
            value: The value to scale
        """
        return value * 10 ** (4 + 2 * self.coeff_number)

    def inverse_scale(self, scaled_value):
        """
        Inverse scale the value of the variable.

        Args:
            scaled_value: The scaled value to inverse scale
        """
        return scaled_value / 10 ** (4 + 2 * self.coeff_number)

    def __str__(self):
        """
        Return a string representation of the variable.

        Returns:
            str: A string representation of the variable.
        """
        return f"Asphere Coeff. {self.coeff_number}, " \
            f"Surface {self.surface_number}"