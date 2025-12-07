import React, { useEffect, useState } from 'react';
import {
  Card,
  Spin,
  Button,
  Tabs,
  message,
  Typography,
  Collapse,
  Modal,
  Input,
} from 'antd';
import { useNavigate } from 'react-router-dom';
import Selectors from './section/Selectors';
import GeneralSetting from './general-setting/GeneralSetting';
import ArticleAuthConfig from './auth/ArticleAuthConfig';
import '../../../components_style/ArticleContentConfiguration.css'
import { fetchArticleContentConfig } from '../../../api/ArticleService';

const { TabPane } = Tabs;
const { Title } = Typography;
const { Panel } = Collapse;

export interface Selector {
  name: string;
  type: string;
  regex?: string[];
  attribute?: string;
}

interface AuthStep {
  name: string;
  type: string;
  action: string;
  elementType: string;
}

export interface Doc {
  id: number;
  name: string;
  language: string;
  login: number;
  newspaperID: number;
  executionMode: string;
  betweenWait: number;
  body: Selector[];
  date: Selector[];
  author: Selector[];
  header: Selector[];
  images: Selector[];
  section: Selector[];
  excludes: Selector[];
  keywords: Selector[];
  paragraphs: Selector[];
  mainsector: Selector[];
  recommendations: Selector[];
  trendingsStories: Selector[];
  cookies: {
    steps: Record<string, Selector & { action: string; elementType: string }>;
    identifier: Selector & { validate: boolean };
  };
  authConfig: {
    authId: number;
    loginUrl: string;
    afterLoginUrl: string;
    siteIdentifier: Selector & { validate: boolean };
    steps: Record<string, AuthStep>;
  };
}

export interface ArticleContentConfigResponse {
  id: number;
  doc: Doc;
  userid: number;
  adddate: string;
  mgroup: number;
}

interface ArticleContentConfigProps {
  newspaperid: number;
  fullView?: boolean;
}

const ArticleSections: React.FC<Doc> = (articleConfig) => {
  const sections = [
    { key: '1', header: 'Header Selectors', content: <Selectors selectors={articleConfig.header} sectionName='Header Selectors' /> },
    { key: '2', header: 'Body Selectors', content: <Selectors selectors={articleConfig.body} sectionName='Body Selectors' /> },
    { key: '3', header: 'Date Selectors', content: <Selectors selectors={articleConfig.date} sectionName='Date Selectors' /> },
    { key: '4', header: 'Author Selectors', content: <Selectors selectors={articleConfig.author} sectionName='Author Selectors' /> },
    { key: '5', header: 'Main Sector', content: <Selectors selectors={articleConfig.mainsector} sectionName='Main Sector' /> },
    { key: '6', header: 'Keywords', content: <Selectors selectors={articleConfig.keywords} sectionName='Keywords' /> },
    { key: '7', header: 'Paragraphs', content: <Selectors selectors={articleConfig.paragraphs} sectionName='Paragraphs' /> },
    { key: '8', header: 'Excludes', content: <Selectors selectors={articleConfig.excludes} sectionName='Excludes' /> },
    { key: '9', header: 'Recommendations', content: <Selectors selectors={articleConfig.recommendations} sectionName='Recommendations' /> },
    { key: '10', header: 'Trending Stories', content: <Selectors selectors={articleConfig.trendingsStories} sectionName='Trending Stories' /> },
  ];

  return (
    <Collapse style={{ paddingTop: '8px', borderRadius: '8px' }}>
      {sections.map(item => (
        <Panel
          header={<span style={{ fontWeight: 'bold' }}>{item.header}</span>}
          key={item.key}
          showArrow={false}
          style={{ marginBottom: '8px', borderRadius: '8px' }}
        >
          <div>{item.content}</div>
        </Panel>
      ))}
    </Collapse>
  );
};

const ArticleContentConfiguration: React.FC<ArticleContentConfigProps> = ({ newspaperid, fullView = false }) => {
  const [config, setConfig] = useState<Doc | null>(null);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [configName, setConfigName] = useState('');
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const fetchConfig = async (newspaperid: number) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetchArticleContentConfig(newspaperid);
      const data: ArticleContentConfigResponse | null = await response;
      if (data?.doc?.newspaperID === newspaperid) {
        setConfig(data.doc);
      } else {
        setConfig(null);
      }
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('Unknown error');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchConfig(newspaperid);
  }, [newspaperid]);

  const updateField = (field: keyof Doc, value: string | boolean | number) => {
    if (config) {
      setConfig({ ...config, [field]: value });
    }
  };

  const handleCreateConfig = async () => {
    try {
      const res = await fetch(`http://localhost:8001/articles/v1/article-config/${newspaperid}/create`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: configName }),
      });
      if (res.ok) {
        message.success('Configuration created!');
        setModalVisible(false);
        fetchConfig(newspaperid);
      } else {
        message.error('Failed to create configuration');
      }
    } catch (error) {
      message.error(`Error creating configuration: ${error instanceof Error ? error.message : ''}`)
    }
  };

  if (loading) return <Spin tip="Loading article config..." style={{ display: 'block', marginTop: 100 }} />;

  if (error) {
    return (
      <Card style={{ marginTop: 100 }}>
        <Title level={4} type="danger">❌ Error loading configuration</Title>
        <p>{error}</p>
      </Card>
    );
  }

  if (!config) {
    return (
      <Card style={{ textAlign: 'center', padding: 60, marginTop: 50 }}>
        <Title level={4} style={{ color: '#999' }}>🗃️ No Configuration Available</Title>
        <p style={{ color: '#aaa', marginBottom: 30 }}>
          This newspaper currently has no content configuration.
        </p>
        <Button type="primary" size="large"
        // onClick={() => setModalVisible(true)}
        >
          ➕ Create Configuration
        </Button>

        <Modal
          title="Create New Configuration"
          open={modalVisible}
          onOk={handleCreateConfig}
          onCancel={() => setModalVisible(false)}
          okText="Create"
        >
          <Input
            placeholder="Enter configuration name"
            value={configName}
            onChange={(e) => setConfigName(e.target.value)}
          />
        </Modal>
      </Card>
    );
  }

  return (
    <Card
      title={<Title level={4}>Article Content Configuration - {config.name}</Title>}
      extra={!fullView && (
        <Button type="primary" onClick={() => navigate(`/article-config/${newspaperid}`)}>
          Full View
        </Button>
      )}
      style={{ borderRadius: 12, boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}
    >
      <Tabs defaultActiveKey="general" type="line">
        <TabPane tab="General" key="general">
          <GeneralSetting config={config} onUpdate={updateField} />
        </TabPane>

        <TabPane tab="Section" key="selectors">
          <ArticleSections {...config} />
        </TabPane>

        {/* <TabPane tab="Auth Config" key="auth" disabled={config.login === 0}>
          <ArticleAuthConfig config={config.authConfig} />
        </TabPane> */}
      </Tabs>
    </Card>
  );
};

export default ArticleContentConfiguration;
