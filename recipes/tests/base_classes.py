from django.test import TestCase


class ModelsTestBase(TestCase):
    def check_field_list(self, instance, field_names, many_to_many=False):
        instance_fields = (
            instance._meta.many_to_many
            if many_to_many else instance._meta.fields)
        instance_field_names = [q.name for q in instance_fields]
        self.assertListEqual(instance_field_names, field_names)

    def check_field_classes(self, instance, field_classes):
        for field, _class in field_classes.items():
            with self.subTest():
                self.assertIsInstance(instance._meta.get_field(field), _class)

    def check_cascade(self, model, foreign_key, foreign_model, fm_instance):
        instance = model.objects.filter(**{foreign_key: fm_instance})
        with self.subTest():
            self.assertTrue(instance.exists())
        foreign_model.objects.get(id=fm_instance.id).delete()
        self.assertFalse(instance.exists())

    def check_related_names(self, instance, relations):
        for related_instance, related_name in relations:
            with self.subTest():
                query = related_instance.__getattribute__(related_name).all()
                self.assertIn(instance, query)

    def check_field_attrs(self, instance, field_attrs, remote=False):
        for field, attrs in field_attrs.items():
            for attr, value in attrs.items():
                with self.subTest():
                    instance_field = (
                        instance._meta.get_field(field).remote_field
                        if remote else instance._meta.get_field(field))
                    self.assertEqual(instance_field.__getattribute__(attr), value)

    def check_model_attrs(self, instance, model_attrs):
        for attr, attr_value in model_attrs.items():
            with self.subTest():
                self.assertEqual(
                    instance._meta.__getattribute__(attr), attr_value)
