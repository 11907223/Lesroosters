class Course():
    def __init__(self, name, lectures, workgroups, max_workgroup, practicals, max_practical, expected) -> None:
        self.name = name
        self.lectures = lectures
        self.max_practical = max_practical
        self.practicals = practicals
        self.workgroups = workgroups
        self.max_workgroup = max_workgroup
        self.expected = expected
    
    def number_of_activities(self):
        '''Returns total number of activities in this course.'''
        
        return len(self.workgroups) + len(self.practicals) + len(self.lectures)

    def all_activities(self):
        '''Returns all activity objects corresponding to this course.'''

        return self.lectures + self.practicals + self.workgroups
