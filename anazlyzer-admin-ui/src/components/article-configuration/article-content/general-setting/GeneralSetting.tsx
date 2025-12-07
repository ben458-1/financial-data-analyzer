import React, { useState } from 'react';
import { Form, Input, Select, Button, Space, Card } from 'antd';
import { Doc } from '../ArticleContentConfiguration';

// const { Text } = Typography;

interface GeneralSettingProps {
    config: Doc;
    languageOptions?: string[];
    onUpdate: (field: string, value: string | boolean | number) => void;
}

const GeneralSetting: React.FC<GeneralSettingProps> = ({ config, onUpdate }) => {
    const [editMode, setEditMode] = useState(false);
    const [form] = Form.useForm();

    const handleSave = async () => {
        try {
            const values = await form.validateFields();
            Object.entries(values).forEach(([key, value]) => {
                onUpdate(key, value);
            });
            setEditMode(false);
        } catch (error) {
            console.error('Validation Failed:', error);
        }
    };

    const handleCancel = () => {
        form.setFieldsValue(config);
        setEditMode(false);
    };

    return (
        <Card
            title="General Settings"
            bordered={false}
            style={{ borderRadius: 12, boxShadow: '0 2px 8px rgba(0,0,0,0.05)' }}
            extra={
                !editMode ? (
                    <Button type="link" onClick={() => setEditMode(true)}>
                        Edit
                    </Button>
                ) : null
            }
        >
            <Form
                form={form}
                layout="vertical"
                initialValues={config}
            >
                <Form.Item label="Language" name="language">
                    <Select
                        disabled={!editMode}
                        options={['English', 'Tamil', 'French', 'Hindi', 'Swedish'].map((lang) => ({ value: lang, label: lang }))}
                        placeholder="Select language"
                    />
                </Form.Item>

                <Form.Item label="Execution Mode" name="executionMode">
                    <Input
                        placeholder="Enter execution mode"
                        readOnly={!editMode}
                        style={{ backgroundColor: !editMode ? '#f5f5f5' : undefined, cursor: !editMode ? 'not-allowed' : 'auto' }}
                    />
                </Form.Item>

                <Form.Item
                    label="Wait Time (ms)"
                    name="betweenWait"
                    rules={[{ type: 'number', min: 0, message: 'Must be a non-negative number' }]}
                >
                    <Input
                        type="number"
                        placeholder="Enter wait time"
                        readOnly={!editMode}
                        style={{ backgroundColor: !editMode ? '#f5f5f5' : undefined, cursor: !editMode ? 'not-allowed' : 'auto' }}
                    />
                </Form.Item>

                <Form.Item label="Login Required" name="login">
                    <Select
                        disabled={!editMode}
                        options={[
                            { label: 'Yes', value: 1 },
                            { label: 'No', value: 0 },
                        ]}
                        placeholder="Login required?"
                    />
                </Form.Item>

                {editMode && (
                    <Form.Item>
                        <Space>
                            <Button type="primary" onClick={handleSave}>Save</Button>
                            <Button onClick={handleCancel}>Cancel</Button>
                        </Space>
                    </Form.Item>
                )}
            </Form>
        </Card>
    );
};

export default GeneralSetting;