## Question 1. Knowing docker tags

Run the command to get information on Docker 

```docker --help```

Now run the command to get help on the "docker build" command:

```docker build --help```

Do the same for "docker run".

Which tag has the following text? - *Automatically remove the container when it exits* 

- `--delete`
- `--rc`
- `--rmc`
- `--rm` - [x]

## Question 2. Understanding docker first run 

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use ```pip list``` ). 

What is version of the package *wheel* ?

- 0.42.0 - [x]
- 1.0.0
- 23.0.1
- 58.1.0


# Prepare Postgres

Run Postgres and load data as shown in the videos
We'll use the green taxi trips from September 2019:

```wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz```

You will also need the dataset with zones:

```wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv```

Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)


## Question 3. Count records 

How many taxi trips were totally made on September 18th 2019?

Tip: started and finished on 2019-09-18. 

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

- 15767 - [x]
- 15612
- 15859
- 89009

### Query:
``` SQL
WITH sep_18th_records AS (
SELECT *
FROM public.green_september_2019
WHERE
	lpep_pickup_datetime::DATE = '2019-09-18'::DATE AND
	lpep_dropoff_datetime::DATE = '2019-09-18'::DATE
	
)

SELECT COUNT(1) FROM sep_18th_records
```

## Question 4. Largest trip for each day

Which was the pick up day with the largest trip distance
Use the pick up time for your calculations.

- 2019-09-18
- 2019-09-16
- 2019-09-26 - [x]
- 2019-09-21


### Query:
``` SQL
SELECT lpep_pickup_datetime::DATE AS day_of_largest_trip
FROM public.green_september_2019
ORDER BY trip_distance DESC
LIMIT 1
```

## Question 5. Three biggest pick up Boroughs

Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown

Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?
 
- "Brooklyn" "Manhattan" "Queens" - [x]
- "Bronx" "Brooklyn" "Manhattan"
- "Bronx" "Manhattan" "Queens" 
- "Brooklyn" "Queens" "Staten Island"

### Query:
``` SQL
WITH sep_18th_records AS (
SELECT *
FROM public.green_september_2019
WHERE
	lpep_pickup_datetime::DATE = '2019-09-18'::DATE AND
	lpep_dropoff_datetime::DATE = '2019-09-18'::DATE
	
)

SELECT
	"Borough",
	SUM(total_amount)
FROM
	sep_18th_records
	INNER JOIN
	public.zones
	ON
	sep_18th_records."PULocationID" =
	public.zones."LocationID"
GROUP BY "Borough"
HAVING SUM(total_amount) > 50000
```

## Question 6. Largest tip

For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

- Central Park
- Jamaica
- JFK Airport - [x]
- Long Island City/Queens Plaza

### Query:
``` SQL
WITH pickups_at_astoria AS (
SELECT *
FROM 
	public.green_september_2019
	INNER JOIN
	public.zones
	ON
		public.green_september_2019."PULocationID" =
		public.zones."LocationID"
WHERE public.zones."Zone" = 'Astoria'
),

largest_astoria_tip AS (
SELECT tip_amount, "DOLocationID"
FROM pickups_at_astoria
WHERE
	lpep_pickup_datetime::DATE
	BETWEEN
		'2019-09-01'::DATE AND
		'2019-09-30'::DATE
ORDER BY tip_amount DESC
LIMIT 1
)

SELECT "Zone"
FROM
	largest_astoria_tip
	INNER JOIN
	public.zones
	ON
		largest_astoria_tip."DOLocationID" =
		public.zones."LocationID"

```

## Question 7. Creating Resources




```
terraform apply
```


google_bigquery_dataset.dataset: Refreshing state... [id=projects/halogen-ethos-596/datasets/nytaxi]

Terraform used the selected providers to generate the following
execution plan. Resource actions are indicated with the following
symbols:
  + create

Terraform will perform the following actions:

  # google_storage_bucket.data-lake-bucket will be created
  + resource "google_storage_bucket" "data-lake-bucket" {
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "US"
      + name                        = "my_storage_nytaxi_123"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + uniform_bucket_level_access = true
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type = "Delete"
            }
          + condition {
              + age                   = 30
              + matches_prefix        = []
              + matches_storage_class = []
              + matches_suffix        = []
              + with_state            = (known after apply)
            }
        }

      + versioning {
          + enabled = true
        }
    }

Plan: 1 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

google_storage_bucket.data-lake-bucket: Creating...
google_storage_bucket.data-lake-bucket: Creation complete after 2s [id=my_storage_nytaxi_123]
