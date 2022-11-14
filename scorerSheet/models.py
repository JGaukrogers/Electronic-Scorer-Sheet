from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.
class Team(models.Model):
    club_number = models.IntegerField(primary_key=True)
    team_name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.team_name} from {self.location}'


class Player(models.Model):
    pass_number = models.IntegerField(primary_key=True)
    player_name = models.CharField(max_length=50)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.player_name}'


class Game(models.Model):
    year = models.PositiveIntegerField()
    game_number = models.CharField(max_length=10)
    location = models.CharField(max_length=50)

    home_team = models.ForeignKey(Team, related_name='home_team', on_delete=models.CASCADE)
    guest_team = models.ForeignKey(Team, related_name='guest_team', on_delete=models.CASCADE)

    class Meta:
        unique_together = [('year', 'game_number')]

    def __str__(self):
        return f'Game nr {self.game_number} played in {self.year}'


class Score(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)


class Cell(models.Model):
    timestamp = models.TimeField()
    inning = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    game_moves = models.CharField(max_length=50)
    player = models.ForeignKey(Score, on_delete=models.CASCADE)
