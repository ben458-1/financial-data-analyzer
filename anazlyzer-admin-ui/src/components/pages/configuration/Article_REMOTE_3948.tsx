import React, { useEffect, useState } from 'react';
import {
  Table,
  Tabs,
  message,
  Input,
  Space,
  Modal,
  Typography,
  Button,
  Form,
  Card,
  Spin
} from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { EyeOutlined, EditOutlined, SaveOutlined, CloseOutlined } from '@ant-design/icons';
import ArticleMetaConfiguration from '../../article-configuration/article-metadata/ArticleMetadataConfiguration';
import ArticleContentConfiguration from '../../article-configuration/article-content/ArticleContentConfiguration';
import ArticleConfigTemplate from '../../article-configuration/config-template/ArticleConfigTemplate';
import { fetchNewspapers } from '../../../api/ArticleService';

const { Search } = Input;
const { Title } = Typography;
const { TabPane } = Tabs;

export interface Newspaper {
  id: number;
  active_hours: string | null;
  add_date: string;
  alexa_global_ranking: number;
  alexa_local_ranking: number;
  alexa_local_region: string;
  currency: string;
  isactive: number;
  link: string;
  logo: string;
  name: string;
  price_month: number | null;
  price_year: number | null;
  time_zone: string | null;
  language_id: number;
  region_id: number;
}

const Article: React.FC = () => {
  const [articles, setArticles] = useState<Newspaper[]>([]);
  const [searchText, setSearchText] = useState('');
  const [filteredArticles, setFilteredArticles] = useState<Newspaper[]>([]);
  const [modalVisible, setModalVisible] = useState(false);
  const [selectedNewspaper, setSelectedNewspaper] = useState<Newspaper | null>(null);
  const [editingKey, setEditingKey] = useState<number | null>(null);
  const [form] = Form.useForm();
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const loadArticles = async () => {
      setLoading(true);
      setError(null);
      try {
        const result = await fetchNewspapers();
        if (result) {
          setArticles(result);
          setFilteredArticles(result);
        } else {
          setError("Failed to fetch newspapers");
        }
      } catch (error) {
        if (error instanceof Error) {
          setError(error.message);
        } else {
          setError("Failed to fetch newspapers");
        }
      } finally {
        setLoading(false);
      }
    };
    loadArticles();
  }, []);

  const handleSearch = (value: string) => {
    setSearchText(value);
    const filtered = articles.filter(article =>
      article.name.toLowerCase().includes(value.toLowerCase())
    );
    setFilteredArticles(filtered);
  };

  const isEditing = (record: Newspaper) => record.id === editingKey;

  const edit = (record: Newspaper) => {
    form.setFieldsValue({ ...record });
    setEditingKey(record.id);
  };

  const cancel = () => {
    setEditingKey(null);
  };

  const save = async (id: number) => {
    try {
      const row = (await form.validateFields()) as Partial<Newspaper>;
      const newData = [...filteredArticles];
      const index = newData.findIndex(item => item.id === id);
      if (index > -1) {
        const item = newData[index];
        const updatedItem = { ...item, ...row };
        newData.splice(index, 1, updatedItem as Newspaper);
        setFilteredArticles(newData);
        setArticles(newData);
        setEditingKey(null);
        message.success('Updated successfully!');
      }
    } catch (err) {
      message.error('Failed to update');
    }
  };

  const handleViewClick = (record: Newspaper) => {
    setSelectedNewspaper(record);
    setModalVisible(true);
  };

  const columns: ColumnsType<Newspaper> = [
    {
      title: 'Name',
      dataIndex: 'name',
      editable: true,
    },
    {
      title: 'Alexa Global Ranking',
      dataIndex: 'alexa_global_ranking',
      editable: true,
    },
    {
      title: 'Alexa Local Ranking',
      dataIndex: 'alexa_local_ranking',
      editable: true,
    },
    {
      title: 'Link',
      dataIndex: 'link',
      editable: true,
      render: (text) => (
        <a href={text} target="_blank" rel="noopener noreferrer">
          {text}
        </a>
      ),
    },
    {
      title: 'Region',
      dataIndex: 'alexa_local_region',
    },
    {
      title: 'Status',
      dataIndex: 'isactive',
      render: (num: number) =>
        num === 1 ? (
          <span style={{ color: '#8cbb81', fontWeight: 500 }}>🟢 Active</span>
        ) : (
          <span style={{ color: '#eb6c6b', fontWeight: 500 }}>🔴 Inactive</span>
        ),
    },
    {
      title: 'Actions',
      dataIndex: 'actions',
      render: (_, record) => {
        const editable = isEditing(record);
        return (
          <Space>
            {editable ? (
              <>
                <Button icon={<SaveOutlined />} onClick={() => save(record.id)} type="link" />
                <Button icon={<CloseOutlined />} onClick={cancel} type="link" />
              </>
            ) : (
              <>
                <Button
                  icon={<EditOutlined />}
                  onClick={() => edit(record)}
                  type="link"
                  disabled={editingKey !== null}
                />
              </>
            )}
            <Button icon={<EyeOutlined />} type="link" onClick={() => handleViewClick(record)} />
          </Space>
        );
      },
    },
  ];

  const mergedColumns = columns.map(col => {
    if (!col.editable) return col;
    return {
      ...col,
      onCell: (record: Newspaper) => ({
        record,
        inputType: typeof record[col.dataIndex as keyof Newspaper] === 'number' ? 'number' : 'text',
        dataIndex: col.dataIndex,
        title: col.title,
        editing: isEditing(record),
      }),
    };
  });

  const EditableCell: React.FC<{
    editing: boolean;
    dataIndex: string;
    title: any;
    inputType: 'number' | 'text';
    record: Newspaper;
    index?: number;
    children: React.ReactNode;
  }> = ({
    editing,
    dataIndex,
    title,
    inputType,
    record,
    index,
    children,
    ...restProps
  }) => {
      return (
        <td {...restProps}>
          {editing ? (
            <Form.Item
              name={dataIndex}
              style={{ margin: 0 }}
              rules={[{ required: true, message: `Please Input ${title}!` }]}
            >
              <Input type={inputType} />
            </Form.Item>
          ) : (
            children
          )}
        </td>
      );
    };

  const contentStyle: React.CSSProperties = {
    padding: 50,
    background: 'rgba(0, 0, 0, 0.05)',
    borderRadius: 4,
  };
  const content = <div style={contentStyle} />;

  if (loading)
    // return (<Spin tip="Loading newspaper..." style={{ display: 'block', marginTop: 100 }} />);
    return (<div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      height: '100vh',
      width: 'auto'
    }}>
      <Spin tip="Please wait..." size="large" > {content}</Spin>
    </div>);

  if (error) {
    return (
      <Card style={{ marginTop: 100 }}>
        <Title level={4} type="danger">❌ Error loading</Title>
        <p>{error}</p>
      </Card>
    );
  }

  return (
    <div>
      <Title level={4} style={{ marginBottom: 16 }}>
        Article Newspapers
      </Title>

      <Space style={{ marginBottom: 16 }}>
        <Search
          placeholder="Search by name"
          onSearch={handleSearch}
          allowClear
          enterButton
          style={{ width: 300 }}
        />
      </Space>

      <Form form={form} component={false}>
        <Table
          components={{ body: { cell: EditableCell } }}
          bordered
          dataSource={filteredArticles}
          columns={mergedColumns}
          rowKey="id"
          scroll={{ x: 1200, y: 47 * 20 }}
          pagination={{ pageSize: 10 }}
        />
      </Form>

      <Modal
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        footer={null}
        title={selectedNewspaper ? `Configure: ${selectedNewspaper.name}` : ''}
        width="95%"
        centered
        destroyOnClose
        style={{ height: '90vh' }}
        bodyStyle={{ overflowY: 'auto', maxHeight: 'calc(90vh - 35px)' }}
      >
        {selectedNewspaper && (
          <Tabs defaultActiveKey="1">
            <TabPane tab="Article Metadata" key="1">
              <ArticleMetaConfiguration newspaperId={selectedNewspaper.id} />
            </TabPane>
            <TabPane tab="Article Content" key="2">
              <ArticleContentConfiguration newspaperid={selectedNewspaper.id} />
            </TabPane>
            <TabPane tab="Configuration Templates" key="3">
              <ArticleConfigTemplate newspaperid={selectedNewspaper.id} />
            </TabPane>
          </Tabs>
        )}
      </Modal>
    </div>
  );
};

export default Article;
