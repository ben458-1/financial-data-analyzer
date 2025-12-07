import React, { useState } from 'react';
import { Layout } from 'antd';
import { Outlet } from 'react-router-dom';
import SideBar from './sidebar/SideBar';

const { Content, Sider } = Layout;

const AppLayout: React.FC = () => {
  const [collapsed, setCollapsed] = useState(false);

  const toggleCollapsed = () => {
    setCollapsed(!collapsed);
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider
        width={250}
        collapsedWidth={90}
        style={{
          background: '#fff',
          borderRight: '1px solid #eee',
          position: 'fixed',
          left: 0,
          top: 0,
          bottom: 0,
          overflow: 'auto',
          transition: 'all 0.3s ease-in-out',
        }}
        collapsed={collapsed}
      >
        <SideBar collapsed={collapsed} toggleCollapsed={toggleCollapsed} />
      </Sider>

      <Layout style={{ marginLeft: collapsed ? 80 : 250, transition: 'margin-left 0.2s' }}>
        <Content style={{ margin: '16px', overflow: 'auto', minHeight: '100vh' }}>
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
};

export default AppLayout;
