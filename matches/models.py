from django.db import models

class MatchResult(models.Model):
    id = models.CharField(primary_key=True, max_length=8)
    country=models.CharField(max_length=100, blank=True, null=True)
    league = models.CharField(max_length=30, blank=True, null=True)
    home_team = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)
    ms1 = models.DecimalField(max_digits=5, decimal_places=2)
    msx = models.DecimalField(max_digits=5, decimal_places=2)
    ms2 = models.DecimalField(max_digits=5, decimal_places=2)
    kg = models.DecimalField(max_digits=5, decimal_places=2)
    over2_5 = models.DecimalField(max_digits=5, decimal_places=2)
    p_3plus= models.DecimalField(max_digits=5, decimal_places=2)
    date = models.CharField(max_length=15)
    time = models.CharField(max_length=5)
    scores_with_pct = models.JSONField()
    half_scores_with_pct = models.JSONField()
    match_result_with_pct = models.JSONField()
    top_5_first_half = models.TextField()
    top_5_final = models.TextField()
    top3_combo = models.TextField()
    home_team_logo = models.CharField(max_length=100)
    away_team_logo = models.CharField(max_length=100)
    home_to_away_count=models.IntegerField(null=True)
    home_to_home_count=models.IntegerField(null=True)
    away_to_home_count=models.IntegerField(null=True)
    away_to_away_count=models.IntegerField(null=True)
    home_to_away_pct=models.DecimalField(max_digits=5, decimal_places=2,null=True)
    home_to_home_pct=models.DecimalField(max_digits=5, decimal_places=2,null=True)
    away_to_home_pct=models.DecimalField(max_digits=5, decimal_places=2,null=True)
    away_to_away_pct=models.DecimalField(max_digits=5, decimal_places=2,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} ({self.date})"

    def to_dict(self):
        return {
            "id": self.id,
            "country":self.country,
            "league": self.league,
            "HomeTeam": self.home_team,
            "AwayTeam": self.away_team,
            "MS1": float(self.ms1),
            "MSX": float(self.msx),
            "MS2": float(self.ms2),
            "KG": float(self.kg),
            "over2_5": float(self.over2_5),
            "p_3plus":float(self.p_3plus),
            "DATE": self.date,
            "TIME": self.time,
            "scores_with_pct": self.scores_with_pct,
            "half_scores_with_pct": self.half_scores_with_pct,
            "match_result_with_pct": self.match_result_with_pct,
            "top_5_first_half": self.top_5_first_half,
            "top_5_final": self.top_5_final,
            "top3_combo": self.top3_combo,
            "home_team_logo": self.home_team_logo,
            "away_team_logo": self.away_team_logo,
            "home_to_away_count":self.home_to_away_count,
            "home_to_home_count":self.home_to_home_count,
            "away_to_home_count":self.away_to_home_count,
            "away_to_away_count":self.away_to_away_count,
            "home_to_away_pct":self.home_to_away_pct,
            "home_to_home_pct":self.home_to_home_pct,
            "away_to_home_pct":self.away_to_home_pct,
            "away_to_away_pct": self.away_to_away_pct,

        }


from django.db import models

class GlobalTeam(models.Model):
    team_name=models.CharField(max_length=100)
    matches_played=models.IntegerField(default=0)
    country=models.CharField(max_length=100)
    wins = models.IntegerField(default=0)
    wins_home = models.IntegerField(default=0)
    wins_away = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    draws_home = models.IntegerField(default=0)
    draws_away = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    losses_home = models.IntegerField(default=0)
    losses_away = models.IntegerField(default=0)
    goals_scored = models.IntegerField(default=0)
    goals_scored_home = models.IntegerField(default=0)
    goals_scored_away = models.IntegerField(default=0)
    corners_total = models.IntegerField(default=0)
    corners_total_home = models.IntegerField(default=0)
    corners_total_away = models.IntegerField(default=0)
    cards_total = models.IntegerField(default=0)
    cards_total_home = models.IntegerField(default=0)
    cards_total_away = models.IntegerField(default=0)
    average_possession = models.IntegerField(default=0)
    average_possession_home = models.IntegerField(default=0)
    average_possession_away = models.IntegerField(default=0)
    shots = models.IntegerField(default=0)
    shots_home = models.IntegerField(default=0)
    shots_away = models.IntegerField(default=0)
    shots_on_target = models.IntegerField(default=0)
    shots_on_target_home = models.IntegerField(default=0)
    shots_on_target_away = models.IntegerField(default=0)
    goals_scored_half_time = models.IntegerField(default=0)
    goals_scored_half_time_home = models.IntegerField(default=0)
    goals_scored_half_time_away = models.IntegerField(default=0)
    leading_at_half_time = models.IntegerField(default=0)
    leading_at_half_time_home = models.IntegerField(default=0)
    leading_at_half_time_away = models.IntegerField(default=0)
    draw_at_half_time = models.IntegerField(default=0)
    draw_at_half_time_home = models.IntegerField(default=0)
    draw_at_half_time_away = models.IntegerField(default=0)
    losing_at_half_time = models.IntegerField(default=0)
    losing_at_half_time_home = models.IntegerField(default=0)
    losing_at_half_time_away = models.IntegerField(default=0)
    over05_count = models.IntegerField(default=0)
    over15_count = models.IntegerField(default=0)
    over25_count = models.IntegerField(default=0)
    over35_count = models.IntegerField(default=0)
    over05_count_home = models.IntegerField(default=0)
    over15_count_home = models.IntegerField(default=0)
    over25_count_home = models.IntegerField(default=0)
    over35_count_home = models.IntegerField(default=0)
    over45_count_home = models.IntegerField(default=0)
    over55_count_home = models.IntegerField(default=0)
    over05_count_away = models.IntegerField(default=0)
    over15_count_away = models.IntegerField(default=0)
    over25_count_away = models.IntegerField(default=0)
    over35_count_away = models.IntegerField(default=0)
    over05_count_half_time = models.IntegerField(default=0)
    over15_count_half_time = models.IntegerField(default=0)
    over25_count_half_time = models.IntegerField(default=0)
    over05_count_half_time_home = models.IntegerField(default=0)
    over15_count_half_time_home = models.IntegerField(default=0)
    over25_count_half_time_home = models.IntegerField(default=0)
    over05_count_half_time_away = models.IntegerField(default=0)
    over15_count_half_time_away = models.IntegerField(default=0)
    over25_count_half_time_away = models.IntegerField(default=0)
    corners_per_match = models.IntegerField(default=0)
    corners_per_match_home = models.IntegerField(default=0)
    corners_per_match_away = models.IntegerField(default=0)
    cards_per_match = models.IntegerField(default=0)
    cards_per_match_home = models.IntegerField(default=0)
    cards_per_match_away = models.IntegerField(default=0)
    xg_for_avg_overall = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    xg_for_avg_home = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    xg_for_avg_away = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    xg_against_avg_overall = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    xg_against_avg_home = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    xg_against_avg_away = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.common_name
    
from django.db import models

class PastMatches(models.Model):
    home_team = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)
    league = models.CharField(max_length=100, blank=True, null=True)
    country=models.CharField(max_length=100, blank=True, null=True)
   
    home_team_goal_count = models.IntegerField(default=0)
    away_team_goal_count = models.IntegerField(default=0)
    
    home_team_goal_count_half_time = models.IntegerField(default=0)
    away_team_goal_count_half_time = models.IntegerField(default=0)
    
    home_team_corner_count = models.IntegerField(default=0)
    away_team_corner_count = models.IntegerField(default=0)
    
    home_team_yellow_cards = models.IntegerField(default=0)
    home_team_red_cards = models.IntegerField(default=0)
    away_team_yellow_cards = models.IntegerField(default=0)
    away_team_red_cards = models.IntegerField(default=0)
    
    home_team_first_half_cards = models.IntegerField(default=0)
    home_team_second_half_cards = models.IntegerField(default=0)
    away_team_first_half_cards = models.IntegerField(default=0)
    away_team_second_half_cards = models.IntegerField(default=0)
    
    home_team_shots = models.IntegerField(default=0)
    away_team_shots = models.IntegerField(default=0)
    
    home_team_shots_on_target = models.IntegerField(default=0)
    away_team_shots_on_target = models.IntegerField(default=0)
    
    home_team_possession = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    away_team_possession = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # CSV'de "Away Team Pre-Match xG" başlığı
    away_team_pre_match_xg = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    team_a_xg = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    team_b_xg = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    date = models.CharField(max_length=15)
    time = models.CharField(max_length=5)
    
    
    def __str__(self):
        return f"{self.home_team_name} vs {self.away_team_name}"    