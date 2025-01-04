# app/tests/test_reports.py
def test_create_report(client):
    # First, register & login to get a token
    client.post('/auth/register', json={
        "username":"testuser","email":"test@example.com","password":"pwd123"
    })
    login_resp = client.post('/auth/login', json={
        "email":"test@example.com","password":"pwd123"
    })
    token = login_resp.get_json()["access_token"]

    # Create a daily report
    resp = client.post('/reports', 
        json={
            "date":"2024-01-10",
            "prayers":[{"prayer_chain_start":"06:00:00", "prayer_chain_end":"06:30:00"}]
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 201