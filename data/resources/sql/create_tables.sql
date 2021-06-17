CREATE TABLE orders (
    id VARCHAR NOT NULL,
    orderNumber INT NOT NULL,
    responsiblePerson VARCHAR NOT NULL,
    healthCareDistrict VARCHAR NOT NULL,
    vaccine VARCHAR NOT NULL,
    injections INT NOT NULL,
    arrived TIMESTAMP NOT NULL,
    PRIMARY KEY (orderNumber)
);

CREATE TABLE vaccinations (
    id VARCHAR NOT NULL,
    sourceBottle VARCHAR NOT NULL,
    gender VARCHAR NOT NULL,
    vaccinationDate TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
);
