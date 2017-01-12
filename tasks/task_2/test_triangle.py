#!/usr/bin/env python
"""Test to checks if provided coordinates belongs to the Right triangle."""

import math
import random


def triangle_coordinates():
    """Generate 6 random int coordinates for 3 triangle points.

    :return: Dict with coordinates.
    """
    min_coord = -100
    max_coord = 100
    return {'X1': random.randint(min_coord, max_coord),
            'Y1': random.randint(min_coord, max_coord),
            'X2': random.randint(min_coord, max_coord),
            'Y2': random.randint(min_coord, max_coord),
            'X3': random.randint(min_coord, max_coord),
            'Y3': random.randint(min_coord, max_coord)}


class TestTriangle(object):
    """Test triangle."""

    round_to = 3

    def is_points_ok(self, **kwargs):
        """Check if each point is unique.

        :param kwargs: Dict with coordinates.
        :return: Boolean.
        """
        point_a = (kwargs['X1'], kwargs['Y1'])
        point_b = (kwargs['X2'], kwargs['Y2'])
        point_c = (kwargs['X3'], kwargs['Y3'])
        points = [point_a, point_b, point_c]
        return all(points.count(x) == 1 for x in points)

    def calculate_len_of_sides(self, Xa, Ya, Xb, Yb, Xc, Yc):
        """Calculate len of triangle sides.

        :param : Coordinates of 3 points.
        :return: 3 float lens.
        """
        AB = math.sqrt(
            ((Xb - Xa) ** 2) + ((Yb - Ya) ** 2))
        AC = math.sqrt(
            ((Xc - Xa) ** 2) + ((Yc - Ya) ** 2))
        BC = math.sqrt(
            ((Xc - Xb) ** 2) + ((Yc - Yb) ** 2))
        return AB, AC, BC

    def do_pifagor_works(self, AB, AC, BC):
        """Check if Pythagorean theorem works with provided data.

        :param AB: len of side 1.
        :param AC: len of side 2.
        :param BC: len of side 3.
        :return: Boolean.
        """
        sides = [AB, AC, BC]
        sides.sort()
        # c= length of the hypotenuse; a,b= lengths of the other two sides.
        a, b, c = sides
        return (
            round((a ** 2 + b ** 2), self.round_to) ==
            round(c ** 2, self.round_to))

    def find_angles(self, AB, AC, BC):
        """Find angles using cosine rule.

        :param AB: len of side 1.
        :param AC: len of side 2.
        :param BC: len of side 3.
        :return: 3 angles in degrees.
        """
        cos_a = (
            (math.fabs(AB) ** 2 + math.fabs(AC) ** 2 - math.fabs(BC) ** 2) /
            (2 * math.fabs(AB) * math.fabs(AC)))
        cos_a = round(cos_a, self.round_to * 2)
        a_rad = math.acos(cos_a)
        a_degr = math.degrees(a_rad)

        cos_b = (
            (math.fabs(AB) ** 2 + math.fabs(BC) ** 2 - math.fabs(AC) ** 2) /
            (2 * math.fabs(AB) * math.fabs(BC)))
        cos_b = round(cos_b, self.round_to * 2)
        b_rad = math.acos(cos_b)
        b_degr = math.degrees(b_rad)

        cos_c = (
            (math.fabs(AC) ** 2 + math.fabs(BC) ** 2 - math.fabs(AB) ** 2) / (
                2 * math.fabs(AC) * math.fabs(BC)))
        cos_c = round(cos_c, self.round_to * 2)
        c_rad = math.acos(cos_c)
        c_degr = math.degrees(c_rad)

        return a_degr, b_degr, c_degr

    def test_is_right_triangle(self):
        """Test if provided coordinates belongs to the right triangle."""
        # generate coordinates
        coords = triangle_coordinates()

        assert self.is_points_ok(**coords), (
            "Triangle can not have 2 or more identical points")

        # calculate len of sides
        sides = self.calculate_len_of_sides(
            Xa=coords['X1'],
            Ya=coords['Y1'],
            Xb=coords['X2'],
            Yb=coords['Y2'],
            Xc=coords['X3'],
            Yc=coords['Y3'])

        # check if Pythagorean theorem works
        pifagor = self.do_pifagor_works(
            AB=sides[0],
            AC=sides[1],
            BC=sides[2])

        # get triangle's angles
        angles = self.find_angles(
            AB=sides[0],
            AC=sides[1],
            BC=sides[2])

        # print information
        print ""
        print "Point A = ({0}, {1})".format(coords['X1'], coords['Y1'])
        print "Point B = ({0}, {1})".format(coords['X2'], coords['Y2'])
        print "Point C = ({0}, {1})".format(coords['X3'], coords['Y3'])

        print "Size AB = {0}".format(round(sides[0], self.round_to))
        print "Size AC = {0}".format(round(sides[1], self.round_to))
        print "Size BC = {0}".format(round(sides[2], self.round_to))

        print "Pythagorean theorem works: {0}".format(pifagor)
        print "Angles: A={angles[0]}, B={angles[1]}, C={angles[2]}".format(
            angles=[round(x, self.round_to) for x in angles])

        assert (pifagor is True and 90 in angles), (
            "\nAccording Pythagorean theorem this triangle is not right.\n"
            "Also there are no 90 degrees angle in this triangle")

    def test_find_coordinates_for_right_triangle(self):
        """Find coordinates of a right triangle."""
        i = 0
        while True:
            i += 1
            coords = triangle_coordinates()

            if self.is_points_ok(**coords) is False:
                continue

            sides = self.calculate_len_of_sides(
                Xa=coords['X1'],
                Ya=coords['Y1'],
                Xb=coords['X2'],
                Yb=coords['Y2'],
                Xc=coords['X3'],
                Yc=coords['Y3'])

            pifagor = self.do_pifagor_works(
                AB=sides[0],
                AC=sides[1],
                BC=sides[2])

            angles = self.find_angles(
                AB=sides[0],
                AC=sides[1],
                BC=sides[2])

            if pifagor is True and 90 in angles:

                print ("\nIt took {0} rounds to find coordinates for the "
                       "right triangle:").format(i)
                print "Point A = ({0}, {1})".format(coords['X1'], coords['Y1'])
                print "Point B = ({0}, {1})".format(coords['X2'], coords['Y2'])
                print "Point C = ({0}, {1})".format(coords['X3'], coords['Y3'])
                print ("Angles: A={angles[0]}, B={angles[1]}, C={angles[2]}"
                       "".format(
                           angles=[round(x, self.round_to) for x in angles]))
                break
