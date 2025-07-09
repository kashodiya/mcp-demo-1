Sure, here are 10 complex analytics queries you can run on the given database schema:

1. **Top 10 Banks with the Highest Number of Submitted Reports:**
   ```sql
   SELECT b.name, COUNT(r.id) AS total_reports
   FROM banks b
   JOIN reports r ON b.id = r.bank_id
   GROUP BY b.name
   ORDER BY total_reports DESC
   LIMIT 10;
   ```

2. **Average Number of Validation Errors per Report by Bank:**
   ```sql
   SELECT b.name, AVG(COUNT(ve.id)) AS avg_errors_per_report
   FROM banks b
   JOIN reports r ON b.id = r.bank_id
   LEFT JOIN validation_errors ve ON r.id = ve.report_id
   GROUP BY b.name;
   ```

3. **Reports with the Most Comments by User:**
   ```sql
   SELECT r.report_code, COUNT(ec.id) AS total_comments, u.username
   FROM reports r
   JOIN validation_errors ve ON r.id = ve.report_id
   JOIN error_comments ec ON ve.id = ec.error_id
   JOIN users u ON ec.user_id = u.id
   GROUP BY r.report_code, u.username
   ORDER BY total_comments DESC
   LIMIT 10;
   ```

4. **Percentage of Accepted Reports by Bank:**
   ```sql
   SELECT b.name, 
          ROUND(SUM(CASE WHEN r.is_accepted = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(r.id), 2) AS pct_accepted
   FROM banks b
   JOIN reports r ON b.id = r.bank_id
   GROUP BY b.name;
   ```

5. **Reports with the Highest Number of Validation Errors:**
   ```sql
   SELECT r.report_code, COUNT(ve.id) AS total_errors
   FROM reports r
   JOIN validation_errors ve ON r.id = ve.report_id
   GROUP BY r.report_code
   ORDER BY total_errors DESC
   LIMIT 10;
   ```

6. **Validation Errors by Error Type and Bank:**
   ```sql
   SELECT b.name, ve.error_type, COUNT(ve.id) AS error_count
   FROM banks b
   JOIN reports r ON b.id = r.bank_id
   JOIN validation_errors ve ON r.id = ve.report_id
   GROUP BY b.name, ve.error_type
   ORDER BY error_count DESC;
   ```

7. **User Activity: Top 10 Users by Number of Comments Made:**
   ```sql
   SELECT u.username, COUNT(ec.id) AS total_comments
   FROM users u
   JOIN error_comments ec ON u.id = ec.user_id
   GROUP BY u.username
   ORDER BY total_comments DESC
   LIMIT 10;
   ```

8. **Reports Submitted on a Specific Date Range:**
   ```sql
   SELECT r.report_code, r.submission_date, b.name
   FROM reports r
   JOIN banks b ON r.bank_id = b.id
   WHERE r.submission_date BETWEEN '2022-01-01' AND '2022-12-31'
   ORDER BY r.submission_date;
   ```

9. **Validation Errors by Field Name and Bank:**
   ```sql
   SELECT b.name, ve.field_name, COUNT(ve.id) AS error_count
   FROM banks b
   JOIN reports r ON b.id = r.bank_id
   JOIN validation_errors ve ON r.id = ve.report_id
   WHERE ve.field_name IS NOT NULL
   GROUP BY b.name, ve.field_name
   ORDER BY error_count DESC;
   ```

10. **Trend of Accepted Reports over Time:**
    ```sql
    SELECT strftime('%Y-%m', r.submission_date) AS month_year, 
           SUM(CASE WHEN r.is_accepted = 1 THEN 1 ELSE 0 END) AS accepted_reports,
           SUM(CASE WHEN r.is_accepted = 0 THEN 1 ELSE 0 END) AS rejected_reports
    FROM reports r
    GROUP BY month_year
    ORDER BY month_year;
    ```

These queries cover a range of analytical tasks, including top performer identification, error analysis, user activity tracking, and trend analysis. They can provide valuable insights into the data and help stakeholders make data-driven decisions.