-- Keep a log of any SQL queries you execute as you solve the mystery.
-- Read description of crime-scene
SELECT description
FROM crime_scene_reports
WHERE month = 7 AND day = 28
AND street = 'Humphrey Street';
-- Read interviews about bakery --> 10:25 am exit, parking lot from 10:15 to 10:25 / ATM on LEgget Street withdraw money / phone call < 1min. Earliest flight tomorrow out Fiftyville. Buy flight ticktet 10:25
SELECT *
FROM interviews
WHERE year = 2023 AND month = 7
AND day >= 28 AND transcrip LIKE '%bakery%';
-- Read bakery sec log after 10:15am -->
SELECT hour, minute, activity, license_plate
FROM bakery_security_logs
WHERE year = 2023
AND month = 7 AND day = 28
AND hour = 10 AND minute BETWEEN 15 AND 25;
 hour | minute | activity | license_plate |
+------+--------+----------+---------------+
| 10   | 16     | exit     | 5P2BI95       |
| 10   | 18     | exit     | 94KL13X       |
| 10   | 18     | exit     | 6P58WS2       |
| 10   | 19     | exit     | 4328GD8       |
| 10   | 20     | exit     | G412CB7       |
| 10   | 21     | exit     | L93JTIZ       |
| 10   | 23     | exit     | 322W7JE       |
| 10   | 23     | exit     | 0NTHK55
--Read ATM transactions
SELECT *
FROM atm_transactions
WHERE year = 2023 AND month = 7 AND day = 28
AND atm_location = 'Leggett Street';
-+
| id  | account_number | year | month | day |  atm_location  | transaction_type | amount |
+-----+----------------+------+-------+-----+----------------+------------------+--------+
| 246 | 28500762       | 2023 | 7     | 28  | Leggett Street | withdraw         | 48     |
| 264 | 28296815       | 2023 | 7     | 28  | Leggett Street | withdraw         | 20     |
| 266 | 76054385       | 2023 | 7     | 28  | Leggett Street | withdraw         | 60     |
| 267 | 49610011       | 2023 | 7     | 28  | Leggett Street | withdraw         | 50     |
| 269 | 16153065       | 2023 | 7     | 28  | Leggett Street | withdraw         | 80     |
| 275 | 86363979       | 2023 | 7     | 28  | Leggett Street | deposit          | 10     |
| 288 | 25506511       | 2023 | 7     | 28  | Leggett Street | withdraw         | 20     |
| 313 | 81061156       | 2023 | 7     | 28  | Leggett Street | withdraw         | 30     |
| 336 | 26013199       | 2023 | 7     | 28  | Leggett Street | withdraw         | 35     |
-- Get the ids of the people of this accounts with a number plate recorded by the securiry_log
    SELECT license_plate
    FROM bakery_security_logs
    WHERE year = 2023
    AND month = 7 AND day = 28
    AND hour = 10 AND minute BETWEEN 15 AND 25)

id   | name  |  phone_number  | passport_number | license_plate |
+--------+-------+----------------+-----------------+---------------+
| 243696 | Barry | (301) 555-4174 | 7526138472      | 6P58WS2       |
| 396669 | Iman  | (829) 555-5269 | 7049073643      | L93JTIZ       |
| 467400 | Luca  | (389) 555-5198 | 8496433585      | 4328GD8       |
| 514354 | Diana | (770) 555-1861 | 3592750733      | 322W7JE       |
| 686048 | Bruce | (367) 555-5533 | 5773159633      | 94KL13X       |
+--------+-------+----------------+-----------------+---------------+

--Identify phone number of tief
SELECT *
FROM phone_calls
WHERE year = 2023
AND month = 7 AND day = 28
AND duration < 60;

--Match passport number and seat
SELECT passport_number, seat
FROM passengers
WHERE flight_id IN (
    SELECT id
    FROM flights
    WHERE year = 2023
    AND month = 7 AND day = 29
);

SELECT *
FROM people
WHERE id IN (
    SELECT person_id
    FROM bank_accounts
    WHERE account_number IN (
        SELECT account_number
        FROM atm_transactions
        WHERE year = 2023 AND month = 7 AND day = 28))
AND license_plate IN (
    SELECT license_plate
    FROM bakery_security_logs
    WHERE year = 2023
    AND month = 7 AND day = 28
    AND hour = 10 AND minute BETWEEN 15 AND 25)
AND phone_number IN (
    SELECT caller
    FROM phone_calls
    WHERE year = 2023
    AND month = 7 AND day = 28
    AND duration < 60)
AND passport_number IN (
    SELECT passport_number
    FROM passengers
    WHERE flight_id IN (
        SELECT id
        FROM flights
        WHERE year = 2023
        AND month = 7 AND day = 29));

        id   | name  |  phone_number  | passport_number | license_plate |
+--------+-------+----------------+-----------------+---------------+
| 514354 | Diana | (770) 555-1861 | 3592750733      | 322W7JE       |
| 686048 | Bruce | (367) 555-5533 | 5773159633      | 94KL13X       |
+--------+-------+----------------+-----------------+---------------+
-- Find out the receiver (complice)
SELECT *
FROM phone_calls
WHERE caller IN (
   SELECT phone_number
   FROM people
   WHERE id IN (514354, 686048)
   )
AND year = 2023
AND month = 7
AND day = 28
AND duration < 60;

-- WHO: BRUCE, COMPLICE: DIANA

--Find where they scaped
SELECT *
FROM airports
WHERE id IN (
    SELECT destination_airport_id
    FROM flights
    WHERE origin_airport_id = (
        SELECT id
        FROM airports
        WHERE city = 'Fiftyville'
    )
    AND id IN (
        SELECT flight_id
        FROM passengers
        WHERE passport_number IN (3592750733, 5773159633)
    )
    AND year = 2023
        AND month = 7 AND day = 29
);

id | abbreviation |          full_name          |     city      |
+----+--------------+-----------------------------+---------------+
| 4  | LGA          | LaGuardia Airport           | New York City |
| 6  | BOS          | Logan International Airport | Boston        |
+----+--------------+-----------------------------+---------------+
