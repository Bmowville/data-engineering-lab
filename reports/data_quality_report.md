# Titanic Data Quality Report

Generated from `data/titanic.db` after the Titanic CSV pipeline runs.

## Summary

| Metric | Value |
| --- | --- |
| Rows | 891 |
| Columns | 12 |
| Missing expected columns | none |
| Duplicate PassengerId values | 0 |

## Missing Values

| Column | Missing Count | Missing Percent |
| --- | --- | --- |
| PassengerId | 0 | 0.0 |
| Survived | 0 | 0.0 |
| Pclass | 0 | 0.0 |
| Name | 0 | 0.0 |
| Sex | 0 | 0.0 |
| Age | 177 | 19.87 |
| SibSp | 0 | 0.0 |
| Parch | 0 | 0.0 |
| Ticket | 0 | 0.0 |
| Fare | 0 | 0.0 |
| Cabin | 687 | 77.1 |
| Embarked | 2 | 0.22 |

## Numeric Ranges

| Column | Minimum | Maximum |
| --- | --- | --- |
| PassengerId | 1 | 891 |
| Survived | 0 | 1 |
| Pclass | 1 | 3 |
| Age | 0.42 | 80.0 |
| SibSp | 0 | 8 |
| Parch | 0 | 6 |
| Fare | 0.0 | 512.3292 |
