-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/zVgQIp
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


CREATE TABLE "Users" (
    "id" INT   NOT NULL,
    "username" VARCHAR   NOT NULL,
    "password" VARCHAR   NOT NULL,
    "email" VARCHAR   NOT NULL,
    "createAt" datetime   NOT NULL,
    "lastLogin" datetime   NOT NULL,
    CONSTRAINT "pk_Users" PRIMARY KEY (
        "id"
     ),
    CONSTRAINT "uc_Users_username" UNIQUE (
        "username"
    ),
    CONSTRAINT "uc_Users_password" UNIQUE (
        "password"
    ),
    CONSTRAINT "uc_Users_email" UNIQUE (
        "email"
    ),
    CONSTRAINT "uc_Users_createAt" UNIQUE (
        "createAt"
    ),
    CONSTRAINT "uc_Users_lastLogin" UNIQUE (
        "lastLogin"
    )
);

CREATE TABLE "Shows" (
    "id" INT   NOT NULL,
    "name" VARCHAR   NOT NULL,
    "rating" INT   NOT NULL,
    "summary" VARCHAR   NOT NULL,
    CONSTRAINT "pk_Shows" PRIMARY KEY (
        "id"
     ),
    CONSTRAINT "uc_Shows_name" UNIQUE (
        "name"
    )
);

CREATE TABLE "Seasons" (
    "id" INT   NOT NULL,
    "numSeason" INT   NOT NULL,
    "showId" INT   NOT NULL,
    CONSTRAINT "pk_Seasons" PRIMARY KEY (
        "id"
     ),
    CONSTRAINT "uc_Seasons_numSeason" UNIQUE (
        "numSeason"
    )
);

CREATE TABLE "Episodes" (
    "id" INT   NOT NULL,
    "name" VARCHAR   NOT NULL,
    "seasonNum" INT   NOT NULL,
    "summary" VARCHAR   NOT NULL,
    "rating" INT   NOT NULL,
    CONSTRAINT "pk_Episodes" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "Watched_shows" (
    "id" INT   NOT NULL,
    "userId" INT   NOT NULL,
    "showId" INT   NOT NULL,
    CONSTRAINT "pk_Watched_shows" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "Watched_episodes" (
    "id" INT   NOT NULL,
    "userId" INT   NOT NULL,
    "episodeId" INT   NOT NULL,
    CONSTRAINT "pk_Watched_episodes" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "Liked_shows" (
    "id" INT   NOT NULL,
    "userId" INT   NOT NULL,
    "showId" INT   NOT NULL,
    CONSTRAINT "pk_Liked_shows" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "Liked_episodes" (
    "id" INT   NOT NULL,
    "userId" INT   NOT NULL,
    "episodeId" INT   NOT NULL,
    CONSTRAINT "pk_Liked_episodes" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "Youtube_vids" (
    "id" INT   NOT NULL,
    "showId" INT   NOT NULL,
    "name" VARCHAR   NOT NULL,
    "url" VARCHAR   NOT NULL,
    "thumbnail" VARCHAR   NOT NULL,
    CONSTRAINT "pk_Youtube_vids" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "Youtube_likes" (
    "id" INT   NOT NULL,
    "userId" INT   NOT NULL,
    "youtubeID" INT   NOT NULL,
    CONSTRAINT "pk_Youtube_likes" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "ShowQueue" (
    "id" INT   NOT NULL,
    "usersID" INT   NOT NULL,
    "showID" INT   NOT NULL,
    "taggedAt" datetime   NOT NULL,
    "interestLevel" INT   NOT NULL,
    CONSTRAINT "pk_ShowQueue" PRIMARY KEY (
        "id"
     )
);

ALTER TABLE "Seasons" ADD CONSTRAINT "fk_Seasons_showId" FOREIGN KEY("showId")
REFERENCES "Shows" ("id");

ALTER TABLE "Episodes" ADD CONSTRAINT "fk_Episodes_seasonNum" FOREIGN KEY("seasonNum")
REFERENCES "Seasons" ("id");

ALTER TABLE "Watched_shows" ADD CONSTRAINT "fk_Watched_shows_userId" FOREIGN KEY("userId")
REFERENCES "Users" ("id");

ALTER TABLE "Watched_shows" ADD CONSTRAINT "fk_Watched_shows_showId" FOREIGN KEY("showId")
REFERENCES "Shows" ("id");

ALTER TABLE "Watched_episodes" ADD CONSTRAINT "fk_Watched_episodes_userId" FOREIGN KEY("userId")
REFERENCES "Users" ("id");

ALTER TABLE "Watched_episodes" ADD CONSTRAINT "fk_Watched_episodes_episodeId" FOREIGN KEY("episodeId")
REFERENCES "Episodes" ("id");

ALTER TABLE "Liked_shows" ADD CONSTRAINT "fk_Liked_shows_userId" FOREIGN KEY("userId")
REFERENCES "Users" ("id");

ALTER TABLE "Liked_shows" ADD CONSTRAINT "fk_Liked_shows_showId" FOREIGN KEY("showId")
REFERENCES "Shows" ("id");

ALTER TABLE "Liked_episodes" ADD CONSTRAINT "fk_Liked_episodes_userId" FOREIGN KEY("userId")
REFERENCES "Users" ("id");

ALTER TABLE "Liked_episodes" ADD CONSTRAINT "fk_Liked_episodes_episodeId" FOREIGN KEY("episodeId")
REFERENCES "Episodes" ("id");

ALTER TABLE "Youtube_vids" ADD CONSTRAINT "fk_Youtube_vids_showId" FOREIGN KEY("showId")
REFERENCES "Shows" ("id");

ALTER TABLE "Youtube_likes" ADD CONSTRAINT "fk_Youtube_likes_userId" FOREIGN KEY("userId")
REFERENCES "Users" ("id");

ALTER TABLE "Youtube_likes" ADD CONSTRAINT "fk_Youtube_likes_youtubeID" FOREIGN KEY("youtubeID")
REFERENCES "Youtube_vids" ("id");

ALTER TABLE "ShowQueue" ADD CONSTRAINT "fk_ShowQueue_usersID" FOREIGN KEY("usersID")
REFERENCES "Users" ("id");

ALTER TABLE "ShowQueue" ADD CONSTRAINT "fk_ShowQueue_showID" FOREIGN KEY("showID")
REFERENCES "Shows" ("id");

