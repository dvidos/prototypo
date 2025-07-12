-- Table: public.events

-- DROP TABLE IF EXISTS public.events;

CREATE TABLE IF NOT EXISTS public.events
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    aggregate_type text COLLATE pg_catalog."default" NOT NULL,
    aggregate_id uuid NOT NULL,
    type text COLLATE pg_catalog."default" NOT NULL,
    payload jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    CONSTRAINT events_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.events
    OWNER to postgres;
