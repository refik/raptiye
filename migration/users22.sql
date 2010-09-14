BEGIN;

ALTER TABLE "users_userprofile" RENAME TO "users_userprofile_old";

CREATE TABLE "subscribed_entries_per_profile" (
    "id" integer NOT NULL PRIMARY KEY,
    "userprofile_id" integer NOT NULL,
    "entry_id" integer NOT NULL,
    UNIQUE ("userprofile_id", "entry_id")
);

CREATE TABLE "users_userprofile" (
    "id" integer NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL UNIQUE,
    "avatar" varchar(200) NOT NULL,
    "web_site" varchar(200) NOT NULL,
    "comments_count" integer unsigned NOT NULL,
    "last_modified" datetime NOT NULL
);

INSERT INTO "users_userprofile"
    SELECT id, user_id, avatar, web_site, 0, last_modified
        FROM "users_userprofile_old";

DROP TABLE "users_userprofile_old";

COMMIT;
