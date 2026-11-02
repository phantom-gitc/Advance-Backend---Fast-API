# Postman Testing Guide

Complete step-by-step instructions to test the FastAPI Authentication & User Management APIs using Postman.

---

## Prerequisites

Make sure your backend server is running in your terminal:

```powershell
cd backend
python -m uvicorn app.main:app --reload
```

- **Base URL:** `http://127.0.0.1:8000`
- **Swagger Docs:** `http://127.0.0.1:8000/docs`

> **Good to Know:** Postman has a built-in cookie jar. When you log in, Postman automatically stores and sends the cookies (`access_token` and `refresh_token`) on all subsequent requests, just like a web browser does.

---

## Step 1: Register a New User

1. Open Postman, click the **`+`** tab to create a new request.
2. Select **`POST`** from the method dropdown.
3. Enter URL: `http://127.0.0.1:8000/api/auth/register`
4. Click the **Body** tab below the URL bar.
5. Choose **`raw`** and select **`JSON`** from the format dropdown.
6. Paste the following JSON payload:
   ```json
   {
     "full_name": "Saroj Kumar",
     "email": "saroj@example.com",
     "password": "StrongPassword123!"
   }
   ```
7. Click **Send**.
8. **Expected Response:** `201 Created`
   ```json
   {
     "success": true,
     "message": "User registered successfully",
     "data": {
       "user": {
         "id": "67269...",
         "full_name": "Saroj Kumar",
         "email": "saroj@example.com",
         "role": "user",
         "is_active": true
       }
     }
   }
   ```

---

## Step 2: Login (Receives Cookies)

1. Create a new request tab in Postman.
2. Select **`POST`** method.
3. Enter URL: `http://127.0.0.1:8000/api/auth/login`
4. In **Body** -> **raw** -> **JSON**, paste:
   ```json
   {
     "email": "saroj@example.com",
     "password": "StrongPassword123!"
   }
   ```
5. Click **Send**.
6. **Expected Response:** `200 OK`
   ```json
   {
     "success": true,
     "message": "Login successful",
     "data": {
       "user": {
         "id": "67269...",
         "full_name": "Saroj Kumar",
         "email": "saroj@example.com",
         "role": "user"
       }
     }
   }
   ```
7. **Verify Cookies:**
   - In the lower response pane, click on the **Cookies** tab.
   - You will see two HTTP-only cookies stored: `access_token` and `refresh_token`.

---

## Step 3: Get Current User Profile

1. Create a new tab.
2. Select **`GET`** method.
3. Enter URL: `http://127.0.0.1:8000/api/auth/me`
4. Leave Headers and Body empty (Postman automatically attaches the `access_token` cookie from Step 2).
5. Click **Send**.
6. **Expected Response:** `200 OK` with your profile data.

---

## Step 4: Update Profile

1. Create a new tab.
2. Select **`PATCH`** method.
3. Enter URL: `http://127.0.0.1:8000/api/users/me`
4. In **Body** -> **raw** -> **JSON**, paste:
   ```json
   {
     "full_name": "Saroj Kumar Padhi"
   }
   ```
5. Click **Send**.
6. **Expected Response:** `200 OK` with the updated name.

---

## Step 5: Refresh Access Token (Token Rotation)

1. Create a new tab.
2. Select **`POST`** method.
3. Enter URL: `http://127.0.0.1:8000/api/auth/refresh-token`
4. Leave Body empty.
5. Click **Send**.
6. **Expected Response:** `200 OK`
   - In the response **Cookies** tab, you will see a fresh rotated `access_token` and `refresh_token`.

---

## Step 6: Logout

1. Create a new tab.
2. Select **`POST`** method.
3. Enter URL: `http://127.0.0.1:8000/api/auth/logout`
4. Leave Body empty.
5. Click **Send**.
6. **Expected Response:** `200 OK`
   ```json
   {
     "success": true,
     "message": "Logout successful"
   }
   ```
7. **Verify Logout:**
   - Return to the `GET http://127.0.0.1:8000/api/auth/me` tab.
   - Click **Send**.
   - It will now return `401 Unauthorized` because the cookies have been cleared and the session was revoked in MongoDB.

---

## Step 7: Testing Admin Endpoints (Optional)

To test admin-only endpoints:
1. Open your MongoDB Atlas database -> `users` collection.
2. Find your user document and edit `"role": "user"` to `"role": "admin"`.
3. Login again in Postman to get a fresh session.
4. Now you can call:
   - **List Users (Paginated):** `GET http://127.0.0.1:8000/api/users/?page=1&limit=10`
   - **Get User by ID:** `GET http://127.0.0.1:8000/api/users/<USER_ID>`
   - **Update User (Admin):** `PATCH http://127.0.0.1:8000/api/users/<USER_ID>` with:
     ```json
     {
       "role": "admin",
       "is_active": true
     }
     ```
   - **Delete User:** `DELETE http://127.0.0.1:8000/api/users/<USER_ID>`

---

## Pro-Tip: Postman Environment Variable

Instead of typing `http://127.0.0.1:8000` repeatedly:
1. In Postman, click **Environments** on the left menu -> **Create Environment** (e.g. `Local Dev`).
2. Add a variable:
   - **Variable:** `base_url`
   - **Initial value:** `http://127.0.0.1:8000`
   - **Current value:** `http://127.0.0.1:8000`
3. Select `Local Dev` from the environment dropdown in the top-right corner.
4. Use `{{base_url}}/api/auth/login` in your requests.

