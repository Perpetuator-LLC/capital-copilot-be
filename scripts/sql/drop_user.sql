BEGIN;
DELETE FROM auth_user WHERE email = 'user@test.com';
COMMIT;
