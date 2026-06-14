-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 07-06-2026 a las 21:16:38
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `ecommerce`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `buyer_profiles`
--

CREATE TABLE `buyer_profiles` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `address` varchar(200) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `status` varchar(20) DEFAULT 'ACTIVE'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `buyer_profiles`
--

INSERT INTO `buyer_profiles` (`id`, `user_id`, `name`, `email`, `address`, `phone`, `created_at`, `status`) VALUES
(1,NULL, 'Karen', 'a23300743@email.com', 'Guadalajara', '3312345678', '2026-05-25 02:26:57', 'ACTIVE'),
(4,NULL, 'Karen', 'karen2@email.com', 'Guadalajara', '3312345678', '2026-05-25 02:33:19', 'ACTIVE'),
(7,NULL, 'Luis', 'luis@email.com', 'Zapopan', '3311111111', '2026-05-25 02:41:02', 'ACTIVE'),
(8,NULL, 'Lala', 'lala@gmail.com', 'Colomos', '3311764365', '2026-05-25 14:36:04', 'ACTIVE'),
(10,NULL, 'Diana', 'diana@gmail.com', 'Colomos', '3311839204', '2026-05-26 02:22:10', 'ACTIVE');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `order_items`
--

CREATE TABLE `order_items` (
  `id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `unit_price` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `order_items`
--

INSERT INTO `order_items` (`id`, `order_id`, `product_id`, `quantity`, `unit_price`, `subtotal`) VALUES
(1, 1, 1, 2, 15000.00, 30000.00),
(2, 2, 2, 1, 7412.00, 7412.00),
(3, 3, 3, 1, 7649.00, 7649.00),
(4, 4, 3, 1, 7649.00, 7649.00),
(5, 5, 2, 4, 7412.00, 29648.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `stock` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `status` varchar(30) DEFAULT 'ACTIVE',
  `image_url` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `products`
--

INSERT INTO `products` (`id`, `name`, `description`, `price`, `stock`, `created_at`, `status`, `image_url`) VALUES
(1, 'string', 'string', 1.00, 0, '2026-05-25 02:26:12', 'ACTIVE', NULL),
(2, 'HP EliteBook 830G7 Laptop ', 'Laptop con Intel', 7412.00, 26, '2026-05-25 14:46:03', 'ACTIVE', NULL),
(3, 'iPad 11', 'Chip A16', 7649.00, 130, '2026-05-26 02:14:05', 'ACTIVE', NULL),
(4, 'iphone 16', '128 gb pink', 12899.00, 20, '2026-05-26 03:18:26', 'ACTIVE', NULL),
(5, 'iphone 16', '128 gb pink', 12899.00, 20, '2026-05-26 03:18:57', 'INACTIVE', NULL),
(6, 'Lenovo Laptop IdeaPad', '16 GB RAM, 512 GB', 14174.00, 20, '2026-05-26 04:58:28', 'ACTIVE', NULL),
(7, 'Apple MacBook Air Chip M4', '16GB RAM 256GB SSD 13 pulgadas Medianoche', 18999.00, 15, '2026-05-26 05:14:16', 'ACTIVE', NULL),
(8, 'Laptop Lenovo reacondicionada', 'Reacondicionada', 9500.00, 5, '2026-06-02 04:52:37', 'ACTIVE', '/uploads/products/d50117d0-4ac8-494f-b32c-38fade73cc4c.jpg');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `purchase_orders`
--

CREATE TABLE `purchase_orders` (
  `id` int(11) NOT NULL,
  `buyer_id` int(11) NOT NULL,
  `status` varchar(50) NOT NULL DEFAULT 'CREATED',
  `total` decimal(10,2) NOT NULL DEFAULT 0.00,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `purchase_orders`
--

INSERT INTO `purchase_orders` (`id`, `buyer_id`, `status`, `total`, `created_at`) VALUES
(1, 1, 'CREATED', 30000.00, '2026-05-25 02:30:36'),
(2, 1, 'CANCELLED', 7412.00, '2026-05-25 15:24:36'),
(3, 10, 'CREATED', 7649.00, '2026-05-26 02:23:30'),
(4, 10, 'CANCELLED', 7649.00, '2026-05-26 02:23:31'),
(5, 1, 'CREATED', 29648.00, '2026-05-26 04:53:38');

-- --------------------------------------------------------

--
-- Estructura del chat de soporte
--
CREATE TABLE `support_conversations` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `status` varchar(20) NOT NULL DEFAULT 'OPEN',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `support_messages` (
  `id` int(11) NOT NULL,
  `conversation_id` int(11) NOT NULL,
  `sender_role` varchar(20) NOT NULL,
  `content` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` varchar(20) NOT NULL DEFAULT 'CUSTOMER',
  `status` varchar(20) NOT NULL DEFAULT 'ACTIVE',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password_hash`, `role`, `status`, `created_at`) VALUES
(1, 'Lola', 'lola@gmail.com', '$2b$12$xv8f8ncLLN2J/urBGEqpAOJku.RGbb9jnVwO0N8KMqbanLjBeQi9q', 'CUSTOMER', 'ACTIVE', '2026-05-26 04:40:50'),
(2, 'Pedro', 'pedro@gmail.com', '$2b$12$o.eMm.LCD28oxxmYJle5Iep0BbtS2zb1gJ2m0k97ItBIVHWqYP9jq', 'CUSTOMER', 'ACTIVE', '2026-05-26 04:42:16'),
(3, 'Admin', 'admin@gmail.com', '$2b$12$AauLA3DdpY8oyFLa006X9ete6eSa.97wuYpcMRZ5OOTt.avtJxFGy', 'ADMIN', 'ACTIVE', '2026-05-26 04:54:43');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `buyer_profiles`
--
ALTER TABLE `buyer_profiles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `uq_buyer_profiles_user_id` (`user_id`);

--
-- Indices de la tabla `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indices de la tabla `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `purchase_orders`
--
ALTER TABLE `purchase_orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `buyer_id` (`buyer_id`);

--
-- Indices de las tablas de soporte
--
ALTER TABLE `support_conversations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_support_conversations_user` (`user_id`);

ALTER TABLE `support_messages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_support_messages_conversation` (`conversation_id`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `buyer_profiles`
--
ALTER TABLE `buyer_profiles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `order_items`
--
ALTER TABLE `order_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `purchase_orders`
--
ALTER TABLE `purchase_orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT del chat de soporte
--
ALTER TABLE `support_conversations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `support_messages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Restricciones para tablas volcadas
--

--
-- Vinculo entre autenticacion y perfil comprador
--
ALTER TABLE `buyer_profiles`
  ADD CONSTRAINT `fk_buyer_profiles_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Relaciones del chat de soporte
--
ALTER TABLE `support_conversations`
  ADD CONSTRAINT `fk_support_conversations_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `support_messages`
  ADD CONSTRAINT `fk_support_messages_conversation` FOREIGN KEY (`conversation_id`) REFERENCES `support_conversations` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `purchase_orders` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);

--
-- Filtros para la tabla `purchase_orders`
--
ALTER TABLE `purchase_orders`
  ADD CONSTRAINT `purchase_orders_ibfk_1` FOREIGN KEY (`buyer_id`) REFERENCES `buyer_profiles` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
