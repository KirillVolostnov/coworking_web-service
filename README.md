# Coworking Booking System

Microservice-based web platform for booking coworking negotiation rooms.

## Services
- `auth_service` - login, JWT, RBAC.
- `room_service` - room catalog and admin CRUD.
- `booking_service` - availability checks and booking constraints.
- `frontend` - React client for users/admins.
- `gateway` - Nginx reverse proxy and single entrypoint.

## Local run
1. Copy `.env.example` to `.env` and adjust secrets.
2. Run:
   - `docker compose up --build`
3. Open [http://localhost](http://localhost).

## Default admin account
- Username: `admin`
- Password: `admin123`

## Test commands
- Auth service: `cd auth_service && python -m pytest`
- Room service: `cd room_service && python -m pytest`
- Booking service: `cd booking_service && python -m pytest`
- Frontend: `cd frontend && npm run test`
