-- Ejecutar una sola vez sobre una base ecommerce existente.
ALTER TABLE buyer_profiles
    ADD COLUMN user_id INT NULL AFTER id,
    ADD UNIQUE KEY uq_buyer_profiles_user_id (user_id),
    ADD CONSTRAINT fk_buyer_profiles_user
        FOREIGN KEY (user_id) REFERENCES users(id);

-- Vincula automaticamente perfiles antiguos cuyo correo coincida con users.
UPDATE buyer_profiles AS buyer
INNER JOIN users AS app_user ON app_user.email = buyer.email
SET buyer.user_id = app_user.id
WHERE buyer.user_id IS NULL;
