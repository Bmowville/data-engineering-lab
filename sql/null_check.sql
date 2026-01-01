SELECT
  SUM(CASE WHEN Age IS NULL THEN 1 ELSE 0 END) AS age_nulls,
  SUM(CASE WHEN Embarked IS NULL THEN 1 ELSE 0 END) AS embarked_nulls
FROM titanic;
