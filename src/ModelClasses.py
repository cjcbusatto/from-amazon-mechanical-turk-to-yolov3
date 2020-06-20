class ModelClasses:
    INVALID_CLASS = -1
    CLASS_NAMES = [
        ('cat', 0),
        ('dog', 1)
    ]

    @staticmethod
    def get_class_index(class_name):
        classes = dict(ModelClasses.CLASS_NAMES)
        try:
            index = classes[class_name]
            return index
        except:
            return ModelClasses.INVALID_CLASS

    @staticmethod
    def count_classes():
        classes = dict(ModelClasses.CLASS_NAMES)
        return len(classes)
