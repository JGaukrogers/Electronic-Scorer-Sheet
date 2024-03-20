from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
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


class TimeOfChange(models.Model):
    inning_in = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    inning_part = models.CharField(max_length=1,
                                   default='T',
                                   validators=[RegexValidator(regex=r'[TBtb]')])
    batsperson = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(9)])

    def save(self, *args, **kwargs):
        self.inning_part = self.inning_part.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(f'{self.inning_in}{self.inning_part}{self.batsperson}')


class LineUp(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    batting_pos = models.PositiveSmallIntegerField(null=True,
        validators=[MinValueValidator(1), MaxValueValidator(9)]
    )

    def __str__(self):
        return f'game: {self.game} batting pos: {self.batting_pos}'
        # return (
        #     f'{self.player} @ position: {self.defensive_position} '
        #     f'(entered: {self.enter_inning})'
        # )

    def __iter__(self):
        return iter([self.game,
                     # self.team,
                     self.batting_pos,
                     # self.player,
                     # self.defensive_position,
                     # self.enter_inning,
                     ])

    # class Meta:
    #     unique_together = [('game', 'team', 'batting_pos')]


class PlayerRow(models.Model):
    line_up_pos = models.ForeignKey(LineUp, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    jersey_number = models.PositiveSmallIntegerField(null=True, blank=True)
    defensive_position = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)]
    )
    enter_inning = models.ForeignKey(TimeOfChange, related_name="enter_inning",
                                     on_delete=models.CASCADE)


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
    game_move_H_1 = models.CharField(max_length=10, null=True, blank=True)
    game_move_1_2 = models.CharField(max_length=10, null=True, blank=True)
    game_move_2_3 = models.CharField(max_length=10, null=True, blank=True)
    game_move_3_H = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f'Inning {self.inning} player {self.score}'


class InningsSummation(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    inning = models.ForeignKey(Inning, on_delete=models.CASCADE, null=True, blank=True)

    runs = models.SmallIntegerField(null=True, blank=True)
    hits = models.SmallIntegerField(null=True, blank=True)
    errors = models.SmallIntegerField(null=True, blank=True)
    left_on_base = models.SmallIntegerField(validators=[MaxValueValidator(3)], null=True, blank=True)
