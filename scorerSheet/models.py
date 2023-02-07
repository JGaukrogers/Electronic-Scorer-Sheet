from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Team(models.Model):
    club_number = models.IntegerField(unique=True)
    team_name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.team_name} from {self.location}'


class Player(models.Model):
    pass_number = models.IntegerField(primary_key=True)
    player_name = models.CharField(max_length=50)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.player_name


class Game(models.Model):
    year = models.PositiveIntegerField()
    game_number = models.CharField(max_length=10)
    location = models.CharField(max_length=50)
    home_team = models.ForeignKey(Team, related_name='home_team',
                                  on_delete=models.CASCADE)
    guest_team = models.ForeignKey(Team, related_name='guest_team',
                                   on_delete=models.CASCADE)

    class Meta:
        unique_together = [('year', 'game_number')]

    def __str__(self):
        return f'Game nr {self.game_number} played in {self.year}'


class Inning(models.Model):
    inning = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return str(self.inning)


class LineUp(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    defensive_position = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)]
    )
    enter_inning = models.ForeignKey(Inning, related_name="enter_inning",
                                     on_delete=models.CASCADE)
    exit_inning = models.ForeignKey(Inning, related_name="exit_inning",
                                    on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return (
            f'{self.player} @ position: {self.defensive_position} '
            f'(entered: {self.enter_inning} exited: {self.exit_inning})'
        )

    def __iter__(self):
        return iter([self.game,
                 self.player,
                 self.defensive_position,
                 self.enter_inning,
                 self.exit_inning,
                     ])



class Cell(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    # btw note that models.CASCADE can destroy a lot of objects recursively
    # when deleting, but I am assuming app won't be designed to delete anything
    # at any point
    # TODO: the user should not control the number of the inning. Make it private?
    inning = models.ForeignKey(Inning, on_delete=models.CASCADE)
    score = models.ForeignKey(LineUp, on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)]
    )
    game_move_H_1 = models.CharField(max_length=50, null=True, blank=True)
    game_move_1_2 = models.CharField(max_length=50, null=True, blank=True)
    game_move_2_3 = models.CharField(max_length=50, null=True, blank=True)
    game_move_3_H = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'Inning {self.inning} player {self.score}'
