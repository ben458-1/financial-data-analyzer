import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
    Card,
    Spin,
    Tabs,
    Button,
    Modal,
    Input,
    message,
} from 'antd';

import Title from 'antd/lib/typography/Title';
import { Selector as SelectorProp } from '../article-content/ArticleContentConfiguration';
import GeneralSetting from './general-setting/GeneralSetting';
import Selectors from './section/Selectors';
import { fetchArticleMetaConfig } from '../../../api/ArticleService';

const { TabPane } = Tabs;

interface NextPopupAction {
    method: string;
    element: SelectorProp;
}

export interface Doc {
    date: SelectorProp[];
    name: string;
    next: NextPopupAction;
    type: string;
    popup: NextPopupAction;
    maxDays: number;
    newsUrl: SelectorProp[];
    headline: SelectorProp[];
    isActive: number;
    language: string;
    maxLoops: number;
    metadata: SelectorProp[];
    preamble: SelectorProp[];
    dateRegex: string;
    searchUri: string;
    timeRegex: string;
    loopSection: SelectorProp[];
    newspaperId: number;
    sectionRank: number;
    dateRegexDesc: string;
    timeRegexDesc: string;
    articleSection: string;
    searcSectorType: SelectorProp[];
}

export interface ArticleMetaConfigProp {
    id: number;
    doc: Doc;
    newspaper_id: number;
    priority: number;
}

const ArticleMetaConfiguration: React.FC<{ newspaperId: number }> = ({ newspaperId }) => {
    const [configMap, setConfigMap] = useState<Map<string, ArticleMetaConfigProp[]> | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [isEmpty, setIsEmpty] = useState(false);
    const [modalVisible, setModalVisible] = useState(false);
    const [newKey, setNewKey] = useState("");

    useEffect(() => {
        const loadMetaConfig = async () => {
            setLoading(true);
            setError(null);
            setIsEmpty(false);

            try {
                const map = await fetchArticleMetaConfig(newspaperId);
                if (!map) {
                    setIsEmpty(true);
                } else {
                    setConfigMap(map);
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

        loadMetaConfig();
    }, [newspaperId]);

    const updateField = (field: keyof Doc, value: string | boolean | number) => {
        console.log(`Field "${field}" updated to:`, value);
        // TODO: Implement state update or API PATCH logic
    };

    const handleCreateConfig = () => {
        // Example POST logic — replace with actual backend endpoint and structure
        axios
            .post(`http://127.0.0.1:8001/article-meta/v1/${newspaperId}/create`, {
                key: newKey,
                newspaperId,
            })
            .then(() => {
                message.success("Configuration created!");
                setModalVisible(false);
                setLoading(true); // Refetch
                setTimeout(() => window.location.reload(), 1000); // Force refresh for demo
            })
            .catch(() => {
                message.error("Failed to create configuration.");
            });
    };

    if (loading) {
        return (
            <Spin
                tip="Loading Metadata config..."
                style={{ display: 'block', marginTop: 100 }}
            />
        );
    }

    if (error) {
        return (
            <Card style={{ marginTop: 100 }}>
                <Title level={4} type="danger">❌ Error loading configuration</Title>
                <p>{error}</p>
            </Card>
        );
    }

    if (isEmpty || !configMap || configMap.size === 0) {
        return (
            <Card style={{ textAlign: 'center', padding: 60, marginTop: 50 }}>
                <Title level={4} style={{ color: '#999' }}>🗃️ No Configuration Available</Title>
                <p style={{ color: '#aaa', marginBottom: 30 }}>
                    This newspaper currently has no metadata configurations.
                </p>
                <Button
                    type="primary"
                    size="large"
                // onClick={() => setModalVisible(true)}
                >
                    ➕ Create Configuration
                </Button>
            </Card>
        );
    }

    const keys: string[] = [...configMap.keys()];

    return (
        <Card
            title={
                <Title level={4}>
                    Article Metadata Configuration - Sample Newspaper
                </Title>
            }
            style={{ borderRadius: 12, boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}
        >
            <Tabs
                defaultActiveKey={keys[0]}
                tabPosition="top"
                type='card'
                items={keys.map((key) => {
                    const doc = configMap.get(key)?.[0]?.doc;
                    return {
                        key,
                        label: key,
                        children: doc ? (
                            <Tabs defaultActiveKey="general" type="line">
                                <TabPane tab="General" key="general">
                                    <GeneralSetting doc={doc} onUpdate={updateField} />
                                </TabPane>
                                <TabPane tab="Section" key="selectors">
                                    <Selectors {...doc}></Selectors>
                                </TabPane>
                            </Tabs>
                        ) : (
                            <div style={{ padding: 16, color: 'red' }}>
                                ⚠️ No document found for "{key}"
                            </div>
                        ),
                    };
                })}
            />
        </Card>
    );
};

export default ArticleMetaConfiguration;
