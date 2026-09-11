from django.test import TestCase, tag

from manudux.models import ApplianceType


class ApplianceTypeModelTest(TestCase):

    def setUp(self):

        ApplianceType.objects.create(name="HVAC", description="Heating and cooling.")
        ApplianceType.objects.create(name="Kitchen", description="Kitchen appliances.")
        ApplianceType.objects.create(
            name="Water Heater", description="Domestic hot water."
        )

    @tag("models", "ApplianceType")
    def test_appliance_type_name(self):
        """Verifies that the appliance type name is correct."""
        at = ApplianceType.objects.get(name="HVAC")
        self.assertEqual(at.name, "HVAC", msg="Appliance Type names should be the same")
        self.assertEqual(
            str(at),
            "HVAC",
            msg=f"Appliance Type name should contain '{at!s}', but got: {at!s}",
        )
        self.assertEqual(
            at.__str__(),
            "HVAC",
            msg="Appliance Type names should be the same as str",
        )

    @tag("models", "ApplianceType")
    def test_appliance_type_description(self):
        """Verifies that the appliance type description is correct."""
        at = ApplianceType.objects.get(name="HVAC")
        self.assertEqual(
            at.description,
            "Heating and cooling.",
            msg=f"appliance type description is wrong. Should be:'{at.description}'.",
        )

    @tag("models", "ApplianceType")
    def test_appliance_type_object_create(self):
        """Verifies that we can create a new appliance type object."""
        ats = ApplianceType.objects.all()
        self.assertEqual(
            len(ats),
            3,
            msg=f"There should be 3 appliance types but {len(ats)} was in the database.",
        )

        at = ApplianceType.objects.create(
            name="Electronics", description="TVs, computers, etc."
        )
        at.save()
        ats = ApplianceType.objects.all()
        self.assertEqual(
            len(ats),
            4,
            msg=f"There should be 4 appliance types but {len(ats)} was in the database.",
        )

    @tag("models", "ApplianceType")
    def test_appliance_type_object_edit(self):
        """Verifies that we can edit an appliance type object."""
        at = ApplianceType.objects.get(name="HVAC")
        at.name = "test-edit"
        at.save()
        self.assertEqual(
            at.name, "test-edit", msg="Appliance type names should be the same as str"
        )

    @tag("models", "ApplianceType")
    def test_appliance_type_object_delete(self):
        """Verifies that we can delete an appliance type object."""
        at = ApplianceType.objects.get(name="HVAC")
        at.delete()
        ats = ApplianceType.objects.all()
        self.assertEqual(
            len(ats),
            2,
            msg=f"There should be 2 appliance types but got {len(ats)} in the database.",
        )

    @tag("models", "ApplianceType")
    def test_appliance_type_description_can_be_blank(self):
        """Verifies that a description can be blank."""
        at = ApplianceType.objects.get(name="Kitchen")
        at.description = ""
        at.save()
        self.assertIs(at.description, "", msg="Description should be able to be blank.")

    @tag("models", "ApplianceType")
    def test_appliance_type_description_can_be_null(self):
        """Verifies that a description can be null."""
        at = ApplianceType.objects.get(name="Kitchen")
        at.description = None
        at.save()
        self.assertIsNone(at.description, msg="Description should be able to be null.")
