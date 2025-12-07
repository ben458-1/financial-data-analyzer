import React from 'react';
import {
  ApartmentOutlined,
  DesktopOutlined,
  HomeOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  PieChartOutlined,
  SettingOutlined,
  NotificationOutlined,
  ReadOutlined,
  ScheduleOutlined
} from '@ant-design/icons';
import type { MenuProps } from 'antd';
import { Button, Menu } from 'antd';
import { useNavigate, useLocation } from 'react-router-dom';

type MenuItem = Required<MenuProps>['items'][number];

const items: MenuItem[] = [
  // { key: 'dashboard', icon: <PieChartOutlined />, label: 'Dashboard' },
  { key: 'home', icon: <HomeOutlined />, label: 'Home' },
  { key: 'monitoring', icon: <DesktopOutlined />, label: 'Monitoring' },
  {
    key: 'sub1',
    label: 'Configuration',
    icon: <ApartmentOutlined />,
    children: [
      { key: 'article', icon: <ReadOutlined />, label: 'Article' },
      { key: 'scheduler', icon: <ScheduleOutlined/>, label: 'Scheduler'}
    ],
  },
  { key: 'alert-system', icon: <NotificationOutlined />, label: 'Alert System' },
  // { key: 'settings', icon: <SettingOutlined />, label: 'Settings' }
];

interface SideBarProps {
  collapsed: boolean;
  toggleCollapsed: () => void;
}

const SideBar: React.FC<SideBarProps> = ({ collapsed, toggleCollapsed }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleMenuClick: MenuProps['onClick'] = (e) => {
    const key = e.key;
    if (key === 'article') {
      navigate(`/configuration/${key}`);
    } else if (key === 'scheduler') {
      navigate(`/configuration/${key}`)
    }
      else {
      navigate(`/${key}`);
    }
  };

  return (
    <nav className="sidebar" role="navigation" style={{ padding: '16px' }}>
      <Button
        onClick={toggleCollapsed}
        style={{
          marginBottom: 16,
          backgroundColor: "#006A71",
          color: 'white',
          borderRadius: 10,
          width: '100%',
        }}
      >
        {collapsed ? <>SP <MenuUnfoldOutlined /></> : <>Spokesperson <MenuFoldOutlined /></>}
      </Button>

      <Menu
        className="my-custom-menu"
        selectedKeys={[location.pathname.split('/')[1]]}
        defaultOpenKeys={['sub1']}
        mode="inline"
        theme="light"
        inlineCollapsed={collapsed}
        items={items}
        onClick={handleMenuClick}
      />
    </nav>
  );
};

export default SideBar;
