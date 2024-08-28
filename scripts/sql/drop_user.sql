BEGIN;
DELETE FROM auth_user WHERE email = 'user@example.com';
DELETE FROM account_emailaddress WHERE email = 'user@example.com';
COMMIT;