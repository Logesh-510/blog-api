import { useEffect, useState } from "react";
import {
  Bell,
  CheckCheck,
  Heart,
  MessageCircle,
  CreditCard,
} from "lucide-react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [token, setToken] = useState(
    localStorage.getItem("access_token")
  );

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [notifications, setNotifications] = useState([]);
  const [isOpen, setIsOpen] = useState(false);

  const [loginError, setLoginError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  // =========================
  // AI Support Chat
  // =========================

  const [isAiOpen, setIsAiOpen] = useState(false);
  const [aiMessage, setAiMessage] = useState("");
  const [aiHistory, setAiHistory] = useState([]);
  const [aiLoading, setAiLoading] = useState(false);

  // =========================
  // Login
  // =========================

  const handleLogin = async (event) => {
    event.preventDefault();

    setLoginError("");
    setIsLoading(true);

    try {
      const formData = new URLSearchParams();

      formData.append("username", username);
      formData.append("password", password);

      const response = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Login failed");
      }

      localStorage.setItem(
        "access_token",
        data.access_token
      );

      setToken(data.access_token);

      setUsername("");
      setPassword("");
    } catch (error) {
      console.error("Login error:", error);
      setLoginError(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  // =========================
  // Logout
  // =========================

  const handleLogout = () => {
    localStorage.removeItem("access_token");

    setToken(null);
    setNotifications([]);
    setIsOpen(false);
    setIsAiOpen(false);
    setAiHistory([]);
  };

  // =========================
  // Notification Icon
  // =========================

  const getNotificationIcon = (type) => {
    switch (type) {
      case "like":
        return <Heart size={18} />;

      case "comment":
        return <MessageCircle size={18} />;

      case "subscription":
        return <CreditCard size={18} />;

      default:
        return <Bell size={18} />;
    }
  };

  // =========================
  // Notification Type Name
  // =========================

  const getNotificationTypeName = (type) => {
    switch (type) {
      case "like":
        return "Like";

      case "comment":
        return "Comment";

      case "subscription":
        return "Subscription";

      default:
        return "Notification";
    }
  };

  // =========================
  // Format Timestamp
  // =========================

  const formatTimestamp = (timestamp) => {
    const notificationDate = new Date(timestamp);
    const now = new Date();

    const differenceInSeconds = Math.floor(
      (now - notificationDate) / 1000
    );

    if (differenceInSeconds < 60) {
      return "Just now";
    }

    const differenceInMinutes = Math.floor(
      differenceInSeconds / 60
    );

    if (differenceInMinutes < 60) {
      return `${differenceInMinutes} ${
        differenceInMinutes === 1 ? "minute" : "minutes"
      } ago`;
    }

    const differenceInHours = Math.floor(
      differenceInMinutes / 60
    );

    if (differenceInHours < 24) {
      return `${differenceInHours} ${
        differenceInHours === 1 ? "hour" : "hours"
      } ago`;
    }

    const differenceInDays = Math.floor(
      differenceInHours / 24
    );

    if (differenceInDays === 1) {
      return "Yesterday";
    }

    if (differenceInDays < 7) {
      return `${differenceInDays} days ago`;
    }

    return notificationDate.toLocaleDateString();
  };

  // =========================
  // Fetch Notifications
  // =========================

  useEffect(() => {
    if (!token) {
      return;
    }

    const fetchNotifications = async () => {
      try {
        const response = await fetch(
          `${API_URL}/notifications/`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (response.status === 401) {
          handleLogout();
          return;
        }

        if (!response.ok) {
          throw new Error(
            "Failed to fetch notifications"
          );
        }

        const data = await response.json();

        if (Array.isArray(data)) {
          setNotifications(data);
        } else {
          console.error(
            "Unexpected notification response:",
            data
          );
        }
      } catch (error) {
        console.error(
          "Error fetching notifications:",
          error
        );
      }
    };

    fetchNotifications();

    const interval = setInterval(
      fetchNotifications,
      10000
    );

    return () => clearInterval(interval);
  }, [token]);

  // =========================
  // Fetch AI Support History
  // =========================

  useEffect(() => {
    if (!token) {
      return;
    }

    const fetchAiHistory = async () => {
      try {
        const response = await fetch(
          `${API_URL}/api/ai-support/history/`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (response.status === 401) {
          handleLogout();
          return;
        }

        if (!response.ok) {
          throw new Error(
            "Failed to fetch AI support history"
          );
        }

        const data = await response.json();

        if (Array.isArray(data)) {
          setAiHistory(data);
        }
      } catch (error) {
        console.error(
          "Error fetching AI support history:",
          error
        );
      }
    };

    fetchAiHistory();
  }, [token]);

  // =========================
  // Send AI Support Message
  // =========================

  const sendAiMessage = async (event) => {
    event.preventDefault();

    const message = aiMessage.trim();

    if (!message || aiLoading) {
      return;
    }

    setAiLoading(true);

    try {
      const response = await fetch(
        `${API_URL}/api/ai-support/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            message: message,
          }),
        }
      );

      if (response.status === 401) {
        handleLogout();
        return;
      }

      if (!response.ok) {
        const errorData = await response
          .json()
          .catch(() => ({}));

        throw new Error(
          errorData.detail ||
            "Failed to get AI support response"
        );
      }

      const data = await response.json();

      setAiHistory((previousHistory) => [
        ...previousHistory,
        data,
      ]);

      setAiMessage("");
    } catch (error) {
      console.error(
        "Error sending AI support message:",
        error
      );
    } finally {
      setAiLoading(false);
    }
  };

  // =========================
  // Mark All As Read
  // =========================

  const markAllAsRead = async () => {
    try {
      const response = await fetch(
        `${API_URL}/notifications/read-all`,
        {
          method: "PATCH",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (response.status === 401) {
        handleLogout();
        return;
      }

      if (!response.ok) {
        throw new Error(
          "Failed to mark notifications as read"
        );
      }

      setNotifications((previousNotifications) =>
        previousNotifications.map(
          (notification) => ({
            ...notification,
            is_read: 1,
          })
        )
      );
    } catch (error) {
      console.error(
        "Error marking notifications as read:",
        error
      );
    }
  };

  // =========================
  // Toggle Read / Unread
  // =========================

  const toggleNotificationRead = async (
    notification
  ) => {
    try {
      const endpoint =
        notification.is_read === 0
          ? `/notifications/${notification.id}/read`
          : `/notifications/${notification.id}/unread`;

      const response = await fetch(
        `${API_URL}${endpoint}`,
        {
          method: "PATCH",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (response.status === 401) {
        handleLogout();
        return;
      }

      if (!response.ok) {
        throw new Error(
          "Failed to update notification"
        );
      }

      setNotifications((previousNotifications) =>
        previousNotifications.map((item) =>
          item.id === notification.id
            ? {
                ...item,
                is_read:
                  notification.is_read === 0
                    ? 1
                    : 0,
              }
            : item
        )
      );
    } catch (error) {
      console.error(
        "Error updating notification:",
        error
      );
    }
  };

  // =========================
  // Login Screen
  // =========================

  if (!token) {
    return (
      <div className="login-page">
        <div className="login-card">
          <h2>Blog Management</h2>

          <p className="login-subtitle">
            Sign in to view your notifications
          </p>

          <form onSubmit={handleLogin}>
            <div className="form-group">
              <label>Username</label>

              <input
                type="text"
                value={username}
                onChange={(event) =>
                  setUsername(event.target.value)
                }
                placeholder="Enter username"
                required
              />
            </div>

            <div className="form-group">
              <label>Password</label>

              <input
                type="password"
                value={password}
                onChange={(event) =>
                  setPassword(event.target.value)
                }
                placeholder="Enter password"
                required
              />
            </div>

            {loginError && (
              <p className="login-error">
                {loginError}
              </p>
            )}

            <button
              type="submit"
              className="login-button"
              disabled={isLoading}
            >
              {isLoading
                ? "Signing in..."
                : "Sign In"}
            </button>
          </form>
        </div>
      </div>
    );
  }

  // =========================
  // Authenticated Application
  // =========================

  return (
    <div className="app">
      <nav className="navbar">
        <h2>Blog Management</h2>

        <div className="navbar-actions">
          <button
            className="notification-button"
            onClick={() => setIsOpen(!isOpen)}
            aria-label="Notifications"
          >
            <Bell size={24} />

            {notifications.filter(
              (notification) =>
                notification.is_read === 0
            ).length > 0 && (
              <span className="notification-badge">
                {
                  notifications.filter(
                    (notification) =>
                      notification.is_read === 0
                  ).length
                }
              </span>
            )}
          </button>

          <button
            className="logout-button"
            onClick={handleLogout}
          >
            Logout
          </button>
        </div>
      </nav>

      {/* =========================
          Notification Center
          ========================= */}

      {isOpen && (
        <div className="notification-dropdown">
          <div className="notification-header">
            <div>
              <h3>Notifications</h3>

              <span className="notification-count">
                {notifications.length} total
              </span>
            </div>

            <button
              className="read-all-button"
              onClick={markAllAsRead}
            >
              <CheckCheck size={16} />
              Read all
            </button>
          </div>

          <div className="notification-list">
            {notifications.length === 0 ? (
              <div className="empty-notifications">
                <Bell size={30} />
                <p>No notifications</p>
              </div>
            ) : (
              notifications.map(
                (notification) => (
                  <div
                    key={notification.id}
                    className={`notification-item ${
                      notification.is_read === 0
                        ? "unread"
                        : ""
                    }`}
                    onClick={() =>
                      toggleNotificationRead(
                        notification
                      )
                    }
                  >
                    <div className="notification-content">
                      <div className="notification-icon">
                        {getNotificationIcon(
                          notification.notification_type
                        )}
                      </div>

                      <div className="notification-text">
                        <div className="notification-type">
                          {getNotificationTypeName(
                            notification.notification_type
                          )}
                        </div>

                        <p>
                          {notification.message}
                        </p>

                        <small>
                          {formatTimestamp(
                            notification.created_at
                          )}
                        </small>
                      </div>

                      {notification.is_read === 0 && (
                        <span className="unread-dot"></span>
                      )}
                    </div>
                  </div>
                )
              )
            )}
          </div>
        </div>
      )}

      {/* =========================
          AI Support Floating Button
          ========================= */}

      <button
        className="ai-support-button"
        onClick={() => setIsAiOpen(!isAiOpen)}
        aria-label="AI Support"
        title="AI Support"
      >
        💬
      </button>

      {/* =========================
          AI Support Chat Popup
          ========================= */}

      {isAiOpen && (
        <div className="ai-support-popup">
          <div className="ai-support-header">
            <div>
              <h3>AI Support</h3>

              <span>
                How can I help you?
              </span>
            </div>

            <button
              className="ai-close-button"
              onClick={() =>
                setIsAiOpen(false)
              }
              aria-label="Close AI Support"
            >
              ×
            </button>
          </div>

          <div className="ai-support-history">
            {aiHistory.length === 0 ? (
              <div className="ai-empty-state">
                <div className="ai-empty-icon">
                  🤖
                </div>

                <h4>
                  Welcome to AI Support
                </h4>

                <p>
                  Ask me about posts,
                  subscriptions, billing,
                  dashboard, or other features.
                </p>
              </div>
            ) : (
              aiHistory.map((chat) => (
                <div
                  key={chat.id}
                  className="ai-chat-item"
                >
                  <div className="ai-user-message">
                    <span className="ai-message-label">
                      You
                    </span>

                    <p>
                      {chat.question}
                    </p>
                  </div>

                  <div className="ai-response-message">
                    <span className="ai-message-label">
                      AI Support
                    </span>

                    <p>
                      {chat.ai_response}
                    </p>
                  </div>
                </div>
              ))
            )}

            {aiLoading && (
              <div className="ai-loading">
                <span>
                  AI is typing...
                </span>
              </div>
            )}
          </div>

          <form
            className="ai-support-input-area"
            onSubmit={sendAiMessage}
          >
            <input
              type="text"
              value={aiMessage}
              onChange={(event) =>
                setAiMessage(event.target.value)
              }
              placeholder="Ask something..."
              disabled={aiLoading}
            />

            <button
              type="submit"
              disabled={
                aiLoading ||
                !aiMessage.trim()
              }
            >
              {aiLoading ? "..." : "Send"}
            </button>
          </form>
        </div>
      )}
    </div>
  );
}

export default App;
