-- CREATING NEW TABLE FOR LINKS ------------------------------------

BEGIN;
CREATE TABLE IF NOT EXISTS "blog_link" (
    "id" integer NOT NULL PRIMARY KEY,
    "title" varchar(50) NOT NULL,
    "description" varchar(200) NOT NULL,
    "url" varchar(200) NOT NULL,
    "window" bool NOT NULL
);
COMMIT;

-- MOVING LINKS ----------------------------------------------------

INSERT INTO "blog_link" SELECT "id", "title", "description", "url", "window" FROM "links_links";

-- CREATING FLATPAGES ----------------------------------------------

BEGIN;
CREATE TABLE "flatpages_flatpage_sites" (
    "id" integer NOT NULL PRIMARY KEY,
    "flatpage_id" integer NOT NULL,
    "site_id" integer NOT NULL REFERENCES "django_site" ("id"),
    UNIQUE ("flatpage_id", "site_id")
)
;
CREATE TABLE "flatpages_flatpage" (
    "id" integer NOT NULL PRIMARY KEY,
    "url" varchar(100) NOT NULL,
    "title" varchar(200) NOT NULL,
    "content" text NOT NULL,
    "enable_comments" bool NOT NULL,
    "template_name" varchar(70) NOT NULL,
    "registration_required" bool NOT NULL,
    "lang" varchar(2) NOT NULL,
    "show_on_homepage" bool NOT NULL
)
;
CREATE INDEX "flatpages_flatpage_url" ON "flatpages_flatpage" ("url");
COMMIT;

-- MOVING FLATPAGE DATA --------------------------------------------

INSERT INTO "flatpages_flatpage" SELECT "id", "url", "title", "content", "enable_comments", "template_name", "registration_required", "tr", "1" FROM "django_flatpage";
INSERT INTO "flatpages_flatpage_sites" SELECT * FROM "django_flatpage_sites";

-- DROPPING FRONTPAGE TABLES ---------------------------------------

DROP TABLE IF EXISTS "django_flatpage";
DROP TABLE IF EXISTS "django_flatpage_sites";

-- DROPPING SOME OTHER TABLES --------------------------------------

DROP TABLE IF EXISTS "frontpage_frontpage";
DROP TABLE IF EXISTS "frontpage_links";
DROP TABLE IF EXISTS "links_linkcategories";
DROP TABLE IF EXISTS "links_links";
DROP TABLE IF EXISTS "links_links_tags";
