import React, { useState } from 'react';
import { Form, Input, Button, Typography, Space, Card, Divider } from 'antd';
import Steps from './login-steps/Steps';

const { Text } = Typography;

interface StepConfig {
    name: string;
    type: string;
    action: string;
    elementType: string;
    stepName?: string;
}

interface SiteIdentifier {
    name: string;
    type: string;
    validate: boolean;
}

interface AuthConfig {
    authId: number;
    loginUrl: string;
    afterLoginUrl: string;
    steps: Record<string, StepConfig>;
    siteIdentifier: SiteIdentifier;
}

interface Props {
    config: AuthConfig;
    // onUpdate: (updated: Partial<AuthConfig>) => void;
}


const ArticleAuthConfig: React.FC<Props> = ({ config }) => {
    const [form] = Form.useForm();
    const [editMode, setEditMode] = useState(false);

    const handleSave = async () => {
        try {
            const values = await form.validateFields();

            const updatedConfig: AuthConfig = {
                ...config,
                ...values,
                steps: convertStepsToObject(values.steps),
            };

            onUpdate(updatedConfig);
            setEditMode(false);
        } catch (err) {
            console.error(err);
        }
    };


    const handleCancel = () => {
        form.setFieldsValue(config);
        setEditMode(false);
    };

    // Convert object to array for Form.List
    const convertStepsToArray = (stepsObj: Record<string, StepConfig>): StepConfig[] => {
        return Object.entries(stepsObj).map(([stepName, step]) => ({
            stepName,
            ...step,
        }));
    };


    // Convert array back to object with keys like email, password, etc.
    const convertStepsToObject = (stepsArray: StepConfig[]): Record<string, StepConfig> => {
        const obj: Record<string, StepConfig> = {};
        stepsArray.forEach(({ stepName, ...rest }) => {
            if (stepName) obj[stepName.trim()] = rest;
        });
        return obj;
    };

    return (
        <Card
            title="Authentication Configuration"
            extra={
                !editMode ? (
                    <Button type="link" onClick={() => setEditMode(true)}>
                        Edit
                    </Button>
                ) : null
            }
            style={{ borderRadius: 12, boxShadow: '0 2px 8px rgba(0,0,0,0.05)' }}
        >
            <Form
                form={form}
                layout="vertical"
                initialValues={{
                    ...config,
                    steps: convertStepsToArray(config.steps),
                }}
                disabled={!editMode}
            >
                <Form.Item label="Auth ID" name="authId">
                    <Input type="number" />
                </Form.Item>

                <Form.Item label="Login URL" name="loginUrl">
                    <Input />
                </Form.Item>

                <Form.Item label="After Login URL" name="afterLoginUrl">
                    <Input />
                </Form.Item>

                <Divider orientation="left">Login Steps</Divider>

                <Steps form={form} editMode={editMode} />

                <Divider orientation="left">Site Identifier</Divider>

                <Form.Item name={['siteIdentifier', 'name']} label="Selector">
                    <Input />
                </Form.Item>

                <Form.Item name={['siteIdentifier', 'type']} label="Selector Type">
                    <Input />
                </Form.Item>

                <Form.Item name={['siteIdentifier', 'validate']} label="Validate" valuePropName="checked">
                    <Input />
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

export default ArticleAuthConfig;
