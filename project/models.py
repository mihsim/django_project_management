from django.db import models
from django.contrib.auth.models import User

progress = (
    ('1', 'Backlog'),
    ('2', 'To do'),
    ('3', 'In Progress'),
    ('4', 'QA'),
    ('5', 'Done')
)

weight = (
    ('1', '2', '3', '4', '5')
)


class Project(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    administrator = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class ProjectParticipants(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ManyToManyField(User)

    def __str__(self):
        return self.project.name


class ProjectParticipantsInvites(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    status = models.CharField(max_length=10, default='Waiting')

    @classmethod
    def add_invite(cls, project_id, from_user_id, to_user_id):
        """
        This function is accessed when project administrator click invite participant button.
        1. Checks that project and users with provided id-s exist
        2. Checks that project does not have to_user as participant
        3. Checks that to_user does not have invitation to participate in project
        4. Save invite
        """

        try:  # 1
            project = Project.objects.get(id=project_id)
            from_user = User.objects.get(id=from_user_id)
            to_user = User.objects.get(id=to_user_id)
        except (Project.DoesNotExist, User.DoesNotExist):
            return "Error", "Bad data provided!"

        try:  # 2
            ProjectParticipants.objects.get(project=project_id, user=to_user)
            return "Error", "This user is already participating!"
        except ProjectParticipants.DoesNotExist:
            pass

        try:  # 3
            invite = cls.objects.get(project=project_id, to_user=to_user_id)
            return "Error", f"This user is invited already, invite status is: {invite.status}"
        except cls.DoesNotExist:
            # 4
            invite = cls(project=project, from_user=from_user, to_user=to_user)
            invite.save()
            return "Success", "Invitation successfully sent."

    @classmethod
    def accept_invite(cls):
        pass

    @classmethod
    def check_participant(cls, project_id, to_user_email):
        """
        Checks if user with given email address is participating to project with given ID

        :param project_id: Primary key to project
        :param to_user_email: Email address to user that will be checked
        :type project_id: int
        :type to_user_email: str
        :return: Returns message text with user instance if user exists.
        :rtype: Tuple(string, string, User instance) or Tuple(string, string, None)
        """
        try:
            to_user = User.objects.get(email=to_user_email)
        except User.DoesNotExist:
            return "Error", "No registered user has that email.", None
        try:
            ProjectParticipants.objects.get(project=project_id, user=to_user)
            return "Error", "This user is already participating!", to_user
        except ProjectParticipants.DoesNotExist:
            pass
        try:
            invite = cls.objects.get(project=project_id, to_user=to_user.id)
            return "Error", f"This user is invited already, invite status is: {invite.status}", to_user
        except cls.DoesNotExist:
            return "Success", "Invitation can be sent.", to_user

    @classmethod
    def delete_invite(cls, project_id, to_user_id):
        try:
            project = Project.objects.get(id=project_id)
            to_user = User.objects.get(id=to_user_id)
            invite = cls.objects.get(project=project, to_user=to_user)
        except (Project.DoesNotExist, User.DoesNotExist, cls.DoesNotExist):
            return "Error", "Bad data provided!"
        invite.delete()
        return "Success", "Invite deleted!"

    def __str__(self):
        return self.project.name


class Sprint(models.Model):
    name = models.CharField(max_length=100)
    date_from = models.DateField()
    date_to = models.DateField()
    planned_story_points = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    story_points = models.CharField(max_length=200)
    assigned_person = models.ManyToManyField(User)
    task_name = models.CharField(max_length=80)

    def __str__(self):
        return self.name
