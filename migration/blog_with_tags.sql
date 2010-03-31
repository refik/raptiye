ALTER TABLE "blog_entry" RENAME TO "hede";

BEGIN;
CREATE TABLE "blog_entry" (
    "id" integer NOT NULL PRIMARY KEY,
    "title" varchar(80) NOT NULL,
    "datetime" datetime NOT NULL,
    "content" text NOT NULL,
    "sticky" bool NOT NULL,
    "language" varchar(2) NOT NULL,
    "published" bool NOT NULL,
    "comments_enabled" bool NOT NULL,
    "slug" varchar(100) NOT NULL,
    "tags" varchar(255) NOT NULL
);
CREATE INDEX IF NOT EXISTS "blog_entry_slug" ON "blog_entry" ("slug");
COMMIT;

INSERT INTO "blog_entry"
    SELECT "id", "title", "datetime", "content", "sticky", "language", "published", "comments_enabled", "slug", "" FROM "hede";

DROP TABLE "hede";