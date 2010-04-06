alter table 'users_userprofile' rename to 'hede';

BEGIN;
CREATE TABLE "users_userprofile" (
    "id" integer NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id"),
    "avatar" varchar(200) NOT NULL,
    "web_site" varchar(200) NOT NULL,
    "activation_key" varchar(100) NOT NULL,
    "last_modified" datetime NOT NULL
)
;
CREATE INDEX IF NOT EXISTS "users_userprofile_user_id" ON "users_userprofile" ("user_id");
COMMIT;

insert into "users_userprofile" select "id","user_id","avatar","web_site","activation_key","last_modified" from "hede";

drop table "hede";
