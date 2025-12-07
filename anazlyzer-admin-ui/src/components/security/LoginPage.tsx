import React, { useEffect, useState } from "react";
import { useMsal } from "@azure/msal-react";
import { AccountInfo } from "@azure/msal-browser";
import { Card, Button, Row, Col, Typography, message } from "antd";
import { useNavigate, Navigate } from "react-router-dom";
import { LoginOutlined } from "@ant-design/icons";
import { useAuth } from "./auth/AuthContext";
import { fetchUserInfo } from "../../api/LoginService";

const { Title, Text } = Typography;

const primaryColor = "rgb(0, 106, 113)";

const LoginPage: React.FC = () => {
    const { user, setUser } = useAuth();
    const { accounts, instance } = useMsal();
    const [loading, setLoading] = useState<boolean>(false);
    const navigate = useNavigate();

    useEffect(() => {
        const checkAndGetUserInfo = async () => {
            const accountList = instance.getAllAccounts();
            if (accountList.length > 0 && !user) {
                await getUserInfo(accountList[0]);
            }
        };

        checkAndGetUserInfo();
    }, [instance]);

    const getUserInfo = async (account: AccountInfo) => {
        setLoading(true);
        try {
            const userInfo = {
                email: account.username,
                name: account.name,
                id: account.localAccountId,
            };

            const response = await fetchUserInfo();
            setUser(response);
            navigate("/");
        } catch (error) {
            console.error(error);
            message.error("Error fetching user info");
        } finally {
            setLoading(false);
        }
    };

    const handleLogin = async () => {
        try {
            const response = await instance.loginPopup({
                scopes: ["user.read"],
                prompt: "select_account"
            });

            const account = instance.getActiveAccount() || response.account;
            if (account) {
                await getUserInfo(account);
            } else {
                message.error("No account information available");
            }
        } catch (error) {
            console.error("Login error:", error);
            message.error("Login failed");
        }
    };

    const handleLogout = () => {
        instance.logoutPopup()
            .then(() => {
                setUser(null);
            })
            .catch((error) => {
                message.error("Logout failed");
                console.error(error);
            });
    };

    if (user) return <Navigate to="/" replace />;

    return (
        <Row
            justify="center"
            align="middle"
            style={{ minHeight: "100vh", backgroundColor: "#f0f2f5" }}
        >
            {/* Left Side - Logo / Branding */}
            <Col
                xs={24}
                sm={10}
                md={8}
                lg={6}
                xl={6}
                style={{
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "center",
                    alignItems: "center",
                    textAlign: "center",
                }}
            >
                <img
                    src="/Euroland_Logo.png"
                    alt="Company Logo"
                    style={{ width: "80%", maxWidth: "250px", marginBottom: "20px" }}
                />
                <Title level={3} style={{ color: primaryColor }}>
                    Get Started with Spokesperson Admin
                </Title>
                <Text type="secondary">
                    Securely login with your Microsoft account to continue.
                </Text>
            </Col>


            {/* Right Side - Login Box */}
            <Col xs={24} sm={14} md={10} lg={8} xl={6}>
                <Card
                    style={{
                        textAlign: "center",
                        boxShadow: "0px 4px 10px rgba(0, 0, 0, 0.1)",
                    }}
                >
                    <Title level={4}>Login</Title>
                    <Button
                        type="primary"
                        block
                        icon={<LoginOutlined />}
                        size="large"
                        style={{
                            marginTop: "10px",
                            backgroundColor: primaryColor,
                            border: "none",
                        }}
                        onClick={handleLogin}
                        loading={loading}
                    >
                        Login with Microsoft
                    </Button>
                </Card>
            </Col>
        </Row>
    );
};

export default LoginPage;
