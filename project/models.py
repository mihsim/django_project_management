from django.db import models

from users.models import MyUser


class Project(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    administrator = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ProjectParticipants(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ManyToManyField(MyUser)

    @classmethod
    def get_project_participants(cls, project):
        """Used to provide assignee selection in Task form."""
        try:
            project_participants = cls.objects.get(project=project)
            return project_participants.user.all()
        except cls.DoesNotExist:
            return MyUser.objects.none()

    def __str__(self):
        return self.project.name


class ProjectParticipantsInvites(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    from_user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="from_user")
    to_user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="to_user")
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
            from_user = MyUser.objects.get(id=from_user_id)
            to_user = MyUser.objects.get(id=to_user_id)
        except (Project.DoesNotExist, MyUser.DoesNotExist):
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
            to_user = MyUser.objects.get(email=to_user_email)
        except MyUser.DoesNotExist:
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

    def __str__(self):
        return f"Project: {self.project.name}. From: {self.from_user.username}. To: {self.to_user.username}."



