# This file is part of Py6S.
#
# Copyright 2012 Robin Wilson and contributors listed in the CONTRIBUTORS file.
#
# Py6S is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Py6S is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Py6S.  If not, see <http://www.gnu.org/licenses/>.

import unittest

from Py6S_rpv4 import (
    AeroProfile,
    AtmosCorr,
    AtmosProfile,
    Geometry,
    GroundReflectance,
    PredefinedWavelengths,
    SixS,
    Wavelength,
)


class Example6STests(unittest.TestCase):
    def test_6s_example1(self):
        # Implements Example_In_1.txt from the 6S distribution in Py6S
        # Tests against manual run of that file

        s = SixS()
        s.geometry = Geometry.User()
        s.geometry.solar_z = 40
        s.geometry.solar_a = 100
        s.geometry.view_z = 45
        s.geometry.view_a = 50
        s.geometry.month = 7
        s.geometry.day = 23

        s.atmos_profile = AtmosProfile.UserWaterAndOzone(3.0, 3.5)
        s.aero_profile = AeroProfile.User(dust=0.25, water=0.25, oceanic=0.25, soot=0.25)

        s.aot550 = 0.5
        s.altitudes.set_target_custom_altitude(0.2)
        s.altitudes.set_sensor_custom_altitude(3.3, aot=0.25)
        s.wavelength = Wavelength(PredefinedWavelengths.AVHRR_NOAA9_B1)

        s.ground_reflectance = GroundReflectance.HeterogeneousLambertian(
            0.5, GroundReflectance.ClearWater, GroundReflectance.GreenVegetation
        )

        s.atmos_corr = AtmosCorr.AtmosCorrBRDFFromReflectance(0.1)
        s.run()
        self.assertAlmostEqual(s.outputs.apparent_radiance, 12.749, delta=0.002)

    def test_6s_example2(self):
        # Implements Example_In_2.txt from the 6S distribution in Py6S
        # Tests against manual run of that file

        s = SixS()
        s.geometry = Geometry.User()
        s.geometry.solar_z = 0
        s.geometry.solar_a = 20
        s.geometry.view_z = 30
        s.geometry.view_a = 0
        s.geometry.month = 8
        s.geometry.day = 22

        s.atmos_profile = AtmosProfile.PredefinedType(AtmosProfile.NoGaseousAbsorption)

        s.aero_profile = AeroProfile.SunPhotometerDistribution(
            [
                0.050000001,
                0.065604001,
                0.086076997,
                0.112939,
                0.148184001,
                0.194428995,
                0.255104989,
                0.334715992,
                0.439173013,
                0.576227009,
                0.756052017,
                0.99199599,
                1.30157101,
                1.707757,
                2.24070191,
                2.93996596,
                3.85745192,
                5.06126022,
                6.64074516,
                8.71314526,
                11.4322901,
                15,
            ],
            [
                0.001338098,
                0.007492487,
                0.026454749,
                0.058904506,
                0.082712278,
                0.073251031,
                0.040950641,
                0.014576218,
                0.003672085,
                0.001576356,
                0.002422644,
                0.004472982,
                0.007452302,
                0.011037065,
                0.014523974,
                0.016981738,
                0.017641816,
                0.016284294,
                0.01335547,
                0.009732267,
                0.006301342,
                0.003625077,
            ],
            [1.47] * 20,
            [0.0093] * 20,
        )

        s.aot550 = 1.0
        s.altitudes.set_target_sea_level()
        s.altitudes.set_sensor_satellite_level()
        s.wavelength = Wavelength(0.550)
        s.ground_reflectance = GroundReflectance.HomogeneousRoujean(0.037, 0.0, 0.133)

        s.run()

        self.assertAlmostEqual(s.outputs.apparent_radiance, 76.999, delta=0.002)
        self.assertAlmostEqual(s.outputs.background_radiance, 10.017, delta=0.002)

    def test_6s_example3(self):
        s = SixS()
        s.geometry = Geometry.Landsat_TM()
        s.geometry.month = 5
        s.geometry.day = 9
        s.geometry.gmt_decimal_hour = 11.222
        s.geometry.latitude = 40
        s.geometry.longitude = 30

        s.atmos_profile = AtmosProfile.PredefinedType(AtmosProfile.MidlatitudeSummer)

        s.aero_profile = AeroProfile.MultimodalLogNormalDistribution(0.001, 20)
        s.aero_profile.add_component(
            0.05,
            2.03,
            0.538,
            [
                1.508,
                1.500,
                1.500,
                1.500,
                1.500,
                1.500,
                1.500,
                1.500,
                1.495,
                1.490,
                1.490,
                1.490,
                1.486,
                1.480,
                1.470,
                1.460,
                1.456,
                1.443,
                1.430,
                1.470,
            ],
            [
                3.24e-07,
                3.0e-08,
                2.86e-08,
                2.51e-08,
                2.2e-08,
                2.0e-08,
                1.0e-08,
                1.0e-08,
                1.48e-08,
                2.0e-08,
                6.85e-08,
                1.0e-07,
                1.25e-06,
                3.0e-06,
                3.5e-04,
                6.0e-04,
                6.86e-04,
                1.7e-03,
                4.0e-03,
                1.4e-03,
            ],
        )
        s.aero_profile.add_component(
            0.0695,
            2.03,
            0.457,
            [
                1.452,
                1.440,
                1.438,
                1.433,
                1.432,
                1.431,
                1.431,
                1.430,
                1.429,
                1.429,
                1.429,
                1.428,
                1.427,
                1.425,
                1.411,
                1.401,
                1.395,
                1.385,
                1.364,
                1.396,
            ],
            [
                1.0e-08,
                1.0e-08,
                1.0e-08,
                1.0e-08,
                1.0e-08,
                1.0e-08,
                1.0e-08,
                1.0e-08,
                1.38e-08,
                1.47e-08,
                1.68e-08,
                1.93e-08,
                4.91e-08,
                1.75e-07,
                9.66e-06,
                1.94e-04,
                3.84e-04,
                1.12e-03,
                2.51e-03,
                1.31e-01,
            ],
        )
        s.aero_profile.add_component(
            0.4,
            2.03,
            0.005,
            [
                1.508,
                1.500,
                1.500,
                1.500,
                1.500,
                1.500,
                1.500,
                1.500,
                1.495,
                1.490,
                1.490,
                1.490,
                1.486,
                1.480,
                1.470,
                1.460,
                1.456,
                1.443,
                1.430,
                1.470,
            ],
            [
                3.24e-07,
                3.0e-08,
                2.86e-08,
                2.51e-08,
                2.2e-08,
                2.0e-08,
                1.0e-08,
                1.0e-08,
                1.48e-08,
                2.0e-08,
                6.85e-08,
                1.0e-07,
                1.25e-06,
                3.0e-06,
                3.5e-04,
                6.0e-04,
                6.86e-04,
                1.7e-03,
                4.0e-03,
                1.4e-03,
            ],
        )

        s.aot550 = 0.8

        s.altitudes.set_target_custom_altitude(2)
        s.altitudes.set_sensor_satellite_level()

        s.wavelength = Wavelength(PredefinedWavelengths.MODIS_B4)

        s.ground_reflectance = GroundReflectance.HomogeneousOcean(11, 30, 35, 3)

        s.run()

        self.assertAlmostEqual(s.outputs.apparent_reflectance, 0.1234623, delta=0.002)

    def test_6s_example4(self):
        s = SixS()

        s.geometry = Geometry.User()
        s.geometry.solar_z = 61.23
        s.geometry.solar_a = 18.78
        s.geometry.solar_a = 0
        s.geometry.view_z = 18.78
        s.geometry.view_a = 159.2
        s.geometry.month = 4
        s.geometry.day = 30

        s.atmos_profile = AtmosProfile.UserWaterAndOzone(0.29, 0.41)
        s.aero_profile = AeroProfile.PredefinedType(AeroProfile.Continental)

        s.aot550 = 0.14

        s.altitudes.set_target_sea_level()
        s.altitudes.set_sensor_satellite_level()

        s.wavelength = Wavelength(PredefinedWavelengths.AVHRR_NOAA11_B1)

        s.ground_reflectance = GroundReflectance.HomogeneousLambertian(
            [
                0.827,
                0.828,
                0.828,
                0.827,
                0.827,
                0.827,
                0.827,
                0.826,
                0.826,
                0.826,
                0.826,
                0.825,
                0.826,
                0.826,
                0.827,
                0.827,
                0.827,
                0.827,
                0.828,
                0.828,
                0.828,
                0.829,
                0.829,
                0.828,
                0.826,
                0.826,
                0.825,
                0.826,
                0.826,
                0.826,
                0.827,
                0.827,
                0.827,
                0.826,
                0.825,
                0.826,
                0.828,
                0.829,
                0.830,
                0.831,
                0.833,
                0.834,
                0.835,
                0.836,
                0.836,
                0.837,
                0.838,
                0.838,
                0.837,
                0.836,
                0.837,
                0.837,
                0.837,
                0.840,
                0.839,
                0.840,
                0.840,
                0.841,
                0.841,
                0.841,
                0.841,
                0.842,
                0.842,
                0.842,
                0.842,
                0.843,
                0.842,
                0.843,
                0.843,
                0.843,
                0.843,
                0.843,
                0.843,
                0.841,
                0.841,
                0.842,
                0.842,
                0.842,
                0.842,
                0.842,
                0.841,
                0.840,
                0.841,
                0.838,
                0.839,
                0.837,
                0.837,
                0.836,
                0.832,
                0.832,
                0.830,
                0.829,
                0.826,
                0.826,
                0.824,
                0.821,
                0.821,
                0.818,
                0.815,
                0.813,
                0.812,
                0.811,
                0.810,
                0.808,
                0.807,
                0.807,
                0.812,
                0.808,
                0.806,
                0.807,
                0.807,
                0.807,
                0.807,
            ]
        )

        s.run()

        self.assertAlmostEqual(s.outputs.apparent_radiance, 170.771, delta=0.002)
