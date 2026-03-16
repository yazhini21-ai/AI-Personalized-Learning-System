class SyllabusManager:
    def __init__(self):
        self.syllabus = {}

    def add_topic(self, subject, topic):
        if subject not in self.syllabus:
            self.syllabus[subject] = []
        self.syllabus[subject].append(topic)

    def remove_topic(self, subject, topic):
        if subject in self.syllabus and topic in self.syllabus[subject]:
            self.syllabus[subject].remove(topic)

    def list_topics(self, subject):
        return self.syllabus.get(subject, [])

    def get_all_syllabus(self):
        return self.syllabus