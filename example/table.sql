CREATE TABLE chicago (
                            ca INT NOT NULL, 
                            community_area_name VARCHAR(50) NOT NULL,
                            percent_of_housing_crowded DECIMAL(10,1) NOT NULL,
                            percent_households_below_poverty DECIMAL(10,1) NOT NULL,
                            percent_aged_16_unemployed DECIMAL(10,1) NOT NULL,
                            percent_aged_25_without_high_school_diploma DECIMAL(10,1) NOT NULL,
                            percent_aged_under_18_or_over_64 DECIMAL(10,1) NOT NULL,
                            per_capita_income_ DECIMAL(10,2),
                            hardship_index DECIMAL(10,2),

                            PRIMARY KEY (ca));
