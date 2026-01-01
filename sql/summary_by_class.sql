SELECT
  Pclass AS passenger_class,
  COUNT(*) AS total_passengers,
  ROUND(AVG(Survived) * 100.0, 2) AS survival_rate_pct
FROM titanic
GROUP BY Pclass
ORDER BY Pclass;
