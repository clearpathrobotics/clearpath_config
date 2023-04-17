from clearpath_config.platform.decorations import Bumper, TopPlate
from clearpath_config.platform.platform import PlatformConfig, Platform
from clearpath_config.tests.test_utils import (
    valid_object_variable_check,
    invalid_object_variable_check,
    assert_not_errors,
)

INVALID_SERIAL_NUMBERS = [
    "randomstring",  # Random String
    "string-with-hyphens",  # String with Hyphens
    "cpr-z100-0001",  # Fake Robot Code with Prefix
    "z100-0001",  # Fake Robot Code w/o Prefix
    "a200-xyz",  # Real Robot Code
]

VALID_SERIAL_NUMBERS = ["cpr-%s-0001" % robot for robot in Platform.ALL] + [
    "%s-0001" % robot for robot in Platform.ALL
]


class TestPlatformConfig:
    pfmconfig = PlatformConfig()

    def test_serial_number(self):
        errors = []
        # Invalid Inputs
        for serial_number in INVALID_SERIAL_NUMBERS:
            try:
                self.pfmconfig.set_serial_number(serial_number)
            except AssertionError:
                pass  # Do nothing, failure is expected
            else:
                errors.append(
                    "Invalid Serial Number %s was incorrectly accepted" % serial_number
                )
        # Valid Inputs
        for serial_number in VALID_SERIAL_NUMBERS:
            try:
                self.pfmconfig.set_serial_number(serial_number)
            except AssertionError as e:
                errors.append(
                    "Valid Serial Number %s was incorrectly rejected with the following message: %s"
                    % (serial_number, e.args[0])
                )
            if (
                serial_number != self.pfmconfig.get_serial_number()
                and serial_number != self.pfmconfig.get_serial_number(True)
            ):
                errors.append(
                    "Valid Serial Number %s was incorrectly set as %s"
                    % (serial_number, self.pfmconfig.get_serial_number())
                )
        assert_not_errors(errors)


# Extension Samples
INVALID_EXTENSIONS = ["string", -10.0]
VALID_EXTENSIONS = [0, "12.3", 12.3]
# Bumper Models
INVALID_BUMPER_MODELS = ["random", 1]
VALID_BUMPER_MODELS = Bumper.MODELS
# A200 Top Plate Models
INVALID_A200_TOP_PLATE_MODELS = ["random", 1]
VALID_A200_TOP_PLATE_MODELS = TopPlate.MODELS


# Test Decorations
class TestDecorations:
    def test_bumper(self):
        errors = []
        # Enable
        bumper = Bumper("bumper")
        try:
            bumper.enable()
        except AssertionError as e:
            errors.append("Enabling bumper failed with message: %s" % e.args[0])
        else:
            if not bumper.enabled:
                errors.append("Enabling bumper did not set enabled variable to True")
        try:
            bumper.disable()
        except AssertionError as e:
            errors.append("Disabling bumper failed with message: %s" % e.args[0])
        else:
            if bumper.enabled:
                errors.append("Disabling bumper did not set enabled variable to False")
        # Extension
        errors.extend(
            invalid_object_variable_check(
                init_test=lambda extension: Bumper("bumper", extension=extension),
                set_test=lambda obj, extension: Bumper.set_extension(
                    obj, extension
                ),
                invalid_entries=INVALID_EXTENSIONS,
            )
        )
        errors.extend(
            valid_object_variable_check(
                init_test=lambda extension: Bumper("bumper", extension=extension),
                set_test=lambda obj, extension: Bumper.set_extension(
                    obj, extension
                ),
                get_func=lambda obj: Bumper.get_extension(obj),
                valid_entries=VALID_EXTENSIONS,
            )
        )
        # Model
        errors.extend(
            invalid_object_variable_check(
                init_test=lambda model: Bumper("bumper", model=model),
                set_test=lambda obj, model: Bumper.set_model(obj, model),
                invalid_entries=INVALID_BUMPER_MODELS,
            )
        )
        errors.extend(
            valid_object_variable_check(
                init_test=lambda model: Bumper("bumper", model=model),
                set_test=lambda obj, model: Bumper.set_model(obj, model),
                get_func=lambda obj: Bumper.get_model(obj),
                valid_entries=VALID_BUMPER_MODELS,
            )
        )
        assert_not_errors(errors)

    def test_top_plate(self):
        errors = []
        # Enable
        try:
            top_plate = TopPlate("top_plate", enabled=True)
        except AssertionError as e:
            errors.append("Valid intialization failed with error: %s" % e.args[0])
        if not top_plate.enabled:
            errors.append("Top plate initalized enabled not set to enabled.")
        try:
            top_plate = TopPlate("top_plate")
            top_plate.enable()
        except AssertionError as e:
            errors.append("Enabling top plate failed with error: %s" % e.args[0])
        if not top_plate.enabled:
            errors.append("Top plate enabled not set to enabled.")
        # Disable
        try:
            top_plate = TopPlate("top_plate", enabled=False)
        except AssertionError as e:
            errors.append("Valid intialization failed with error: %s" % e.args[0])
        if top_plate.enabled:
            errors.append("Top plate initalized disabled not set to disabled.")
        try:
            top_plate = TopPlate("top_plate")
            top_plate.disable()
        except AssertionError as e:
            errors.append("Disabling top plate failed with error: %s" % e.args[0])
        if top_plate.enabled:
            errors.append("Top plate disabled not set to disabled.")
        # Models
        errors.extend(
            invalid_object_variable_check(
                init_test=lambda model: TopPlate("top_plate", model=model),
                set_test=lambda obj, model: TopPlate.set_model(
                    obj, model
                ),
                invalid_entries=INVALID_A200_TOP_PLATE_MODELS,
            )
        )
        errors.extend(
            valid_object_variable_check(
                init_test=lambda model: TopPlate("top_plate", model=model),
                set_test=lambda obj, model: TopPlate.set_model(
                    obj, model
                ),
                get_func=lambda obj: TopPlate.get_model(obj),
                valid_entries=VALID_A200_TOP_PLATE_MODELS,
            )
        )
        assert_not_errors(errors)

"""
# Heights
INVALID_HEIGHTS = ["string", -1.0]
VALID_HEIGHTS = [0, "0.1", 10.0]
# Rows
INVALID_ROWS = ["string", 2.3, 0]
VALID_ROWS = ["1", 2, 3.0]
# Levels
INVALID_LEVELS = ["string", 2.3, 0]
VALID_LEVELS = ["1", 2, 3.0]
# Bracket Models
INVALID_BRACKET_MODELS = ["default", 1]
VALID_BRACKET_MODELS = PACS.Bracket.MODELS
# FullRisers
INVALID_FULL_RISERS = [[PACS.FullRiser(1), PACS.FullRiser(1)]]
VALID_FULL_RISERS = [
    [PACS.FullRiser(1), PACS.FullRiser(2, 0.2), PACS.FullRiser(3, 0.2)]
]
# RowRisers
INVALID_ROW_RISERS = [[PACS.RowRiser(1, 1), PACS.RowRiser(1, 1)]]
VALID_ROW_RISERS = [
    [PACS.RowRiser(1, 1, 0.1), PACS.RowRiser(1, 2, 0.2), PACS.RowRiser(2, 2, 0.2)]
]
# Brackets
INVALID_BRACKETS = [[PACS.Bracket("duplicate"), PACS.Bracket("duplicate")]]
VALID_BRACKETS = [[PACS.Bracket("bracket1"), PACS.Bracket("bracket2")]]


class TestPACS:
    def test_full_riser(self):
        errors = []
        # Level
        errors.extend(
            invalid_object_variable_check(
                init_test=lambda level: PACS.FullRiser(level=level),
                set_test=lambda obj, level: PACS.FullRiser.set_level(obj, level),
                invalid_entries=INVALID_LEVELS,
            )
        )
        errors.extend(
            valid_object_variable_check(
                init_test=lambda level: PACS.FullRiser(level=level),
                set_test=lambda obj, level: PACS.FullRiser.set_level(obj, level),
                get_func=lambda obj: PACS.FullRiser.get_level(obj),
                valid_entries=VALID_LEVELS,
            )
        )
        # Height
        errors.extend(
            invalid_object_variable_check(
                init_test=lambda height: PACS.FullRiser(level=1, height=height),
                set_test=lambda obj, height: PACS.FullRiser.set_height(obj, height),
                invalid_entries=INVALID_HEIGHTS,
            )
        )
        errors.extend(
            valid_object_variable_check(
                init_test=lambda height: PACS.FullRiser(level=1, height=height),
                set_test=lambda obj, height: PACS.FullRiser.set_height(obj, height),
                get_func=lambda obj: PACS.FullRiser.get_height(obj),
                valid_entries=VALID_HEIGHTS,
            )
        )
        assert_not_errors(errors)

    def test_row_riser(self):
        errors = []
        # Level
        errors.extend(
            invalid_object_variable_check(
                init_test=lambda level: PACS.RowRiser(level=level, row=1),
                set_test=lambda obj, level: PACS.RowRiser.set_level(obj, level),
                invalid_entries=INVALID_LEVELS,
            )
        )
        errors.extend(
            valid_object_variable_check(
                init_test=lambda level: PACS.RowRiser(level=level, row=1),
                set_test=lambda obj, level: PACS.RowRiser.set_level(obj, level),
                get_func=lambda obj: PACS.RowRiser.get_level(obj),
                valid_entries=VALID_LEVELS,
            )
        )
        # Row
        errors.extend(
            invalid_object_variable_check(
                init_test=lambda row: PACS.RowRiser(level=1, row=row),
                set_test=lambda obj, row: PACS.RowRiser.set_row(obj, row),
                invalid_entries=INVALID_ROWS,
            )
        )
        errors.extend(
            valid_object_variable_check(
                init_test=lambda row: PACS.RowRiser(level=1, row=row),
                set_test=lambda obj, row: PACS.RowRiser.set_row(obj, row),
                get_func=lambda obj: PACS.RowRiser.get_row(obj),
                valid_entries=VALID_ROWS,
            )
        )
        # Height
        errors.extend(
            invalid_object_variable_check(
                init_test=lambda height: PACS.RowRiser(level=1, row=1, height=height),
                set_test=lambda obj, height: PACS.RowRiser.set_height(obj, height),
                invalid_entries=INVALID_HEIGHTS,
            )
        )
        errors.extend(
            valid_object_variable_check(
                init_test=lambda height: PACS.RowRiser(level=1, row=1, height=height),
                set_test=lambda obj, height: PACS.RowRiser.set_height(obj, height),
                get_func=lambda obj: PACS.RowRiser.get_height(obj),
                valid_entries=VALID_HEIGHTS,
            )
        )
        assert_not_errors(errors)

    def test_bracket(self):
        # Does not test Accessory components of bracket
        errors = []
        # Model
        errors.extend(
            invalid_object_variable_check(
                init_test=lambda model: PACS.Bracket(name="test", model=model),
                set_test=lambda obj, model: PACS.Bracket.set_model(obj, model),
                invalid_entries=INVALID_BRACKET_MODELS,
            )
        )
        errors.extend(
            valid_object_variable_check(
                init_test=lambda model: PACS.Bracket(name="test", model=model),
                set_test=lambda obj, model: PACS.Bracket.set_model(obj, model),
                get_func=lambda obj: PACS.Bracket.get_model(obj),
                valid_entries=VALID_BRACKET_MODELS,
            )
        )
        # Extension
        errors.extend(
            invalid_object_variable_check(
                init_test=lambda ext: PACS.Bracket(name="test", extension=ext),
                set_test=lambda obj, ext: PACS.Bracket.set_extension(obj, ext),
                invalid_entries=INVALID_EXTENSIONS,
            )
        )
        errors.extend(
            valid_object_variable_check(
                init_test=lambda ext: PACS.Bracket(name="test", extension=ext),
                set_test=lambda obj, ext: PACS.Bracket.set_extension(obj, ext),
                get_func=lambda obj: PACS.Bracket.get_extension(obj),
                valid_entries=VALID_EXTENSIONS,
            )
        )
        assert_not_errors(errors)


    def test_full_risers_config(self):
        errors = []
        # Full Risers
        errors.extend(
            invalid_object_variable_check(
                init_test=lambda full_risers: FullRisersConfig(full_risers=full_risers),
                set_test=lambda obj, full_risers: FullRisersConfig.set_full_risers(
                    obj, full_risers
                ),
                invalid_entries=INVALID_FULL_RISERS,
            )
        )
        errors.extend(
            valid_object_variable_check(
                init_test=lambda full_risers: FullRisersConfig(full_risers=full_risers),
                set_test=lambda obj, full_risers: FullRisersConfig.set_full_risers(
                    obj, full_risers
                ),
                get_func=lambda obj: FullRisersConfig.get_full_risers(obj),
                valid_entries=VALID_FULL_RISERS,
            )
        )
        # Remove
        flrconfig = FullRisersConfig(full_risers=VALID_FULL_RISERS[0])
        flrconfig.remove_full_riser(VALID_FULL_RISERS[0][0])
        if flrconfig.get_full_risers() != VALID_FULL_RISERS[0][1:]:
            errors.append("Failed to remove riser")
        assert_not_errors(errors)

    def test_row_risers_config(self):
        errors = []
        # Row Risers
        errors.extend(
            invalid_object_variable_check(
                init_test=lambda row_risers: RowRisersConfig(row_risers=row_risers),
                set_test=lambda obj, row_risers: RowRisersConfig.set_row_risers(
                    obj, row_risers
                ),
                invalid_entries=INVALID_ROW_RISERS,
            )
        )
        errors.extend(
            valid_object_variable_check(
                init_test=lambda row_risers: RowRisersConfig(row_risers=row_risers),
                set_test=lambda obj, row_risers: RowRisersConfig.set_row_risers(
                    obj, row_risers
                ),
                get_func=lambda obj: RowRisersConfig.get_row_risers(obj),
                valid_entries=VALID_ROW_RISERS,
            )
        )
        # Remove
        rwrconfig = RowRisersConfig(row_risers=VALID_ROW_RISERS[0])
        rwrconfig.remove_row_riser(VALID_ROW_RISERS[0][0])
        if rwrconfig.get_row_risers() != VALID_ROW_RISERS[0][1:]:
            errors.append("Failed to remove riser")
        assert_not_errors(errors)

    def test_brackets_config(self):
        errors = []
        # Brackets
        errors.extend(
            invalid_object_variable_check(
                init_test=lambda brackets: BracketsConfig(brackets),
                set_test=lambda obj, brackets: BracketsConfig.set_brackets(
                    obj, brackets
                ),
                invalid_entries=INVALID_BRACKETS,
            )
        )
        errors.extend(
            valid_object_variable_check(
                init_test=lambda brackets: BracketsConfig(brackets),
                set_test=lambda obj, brackets: BracketsConfig.set_brackets(
                    obj, brackets
                ),
                get_func=lambda obj: BracketsConfig.get_brackets(obj),
                valid_entries=VALID_BRACKETS,
            )
        )
        # Remove
        bktconfig = BracketsConfig(brackets=VALID_BRACKETS[0])
        bktconfig.remove_bracket(bracket=VALID_BRACKETS[0][0])
        if bktconfig.get_brackets() != VALID_BRACKETS[0][1:]:
            errors.append("Failed to remove riser")
        assert_not_errors(errors)
"""
