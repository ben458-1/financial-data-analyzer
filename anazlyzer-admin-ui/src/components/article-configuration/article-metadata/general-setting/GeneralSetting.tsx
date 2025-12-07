import React, { useEffect, useState } from 'react';
import { Form, Input, Select, Button, Space } from 'antd';
import { Doc } from '../ArticleMetadataConfiguration';


const GeneralSetting: React.FC<{ doc: Doc; onUpdate: (field: string, value: string | boolean | number) => void; }> = ({ doc, onUpdate }) => {
    const [editMode, setEditMode] = useState(false);
    const [form] = Form.useForm();

    useEffect(() => {
        form.setFieldsValue(doc);
    }, [doc]);

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
        form.setFieldsValue(doc);
        setEditMode(false);
    };

    return (
        <>
            <Form form={form} layout="vertical" initialValues={doc}>
                <Form.Item label="Section Name" name="articleSection">
                    <Input
                        placeholder="Enter section name"
                        readOnly={!editMode}
                        style={{
                            backgroundColor: !editMode ? '#f5f5f5' : undefined,
                            cursor: !editMode ? 'not-allowed' : 'auto',
                        }}
                    />
                </Form.Item>

                <Form.Item label="Language" name="language">
                    <Select
                        disabled={!editMode}
                        options={['English', 'Tamil', 'French', 'Hindi', 'Swedish'].map(
                            (lang) => ({ value: lang, label: lang })
                        )}
                        placeholder="Select language"
                    />
                </Form.Item>

                <Form.Item label="Execution Mode" name="type">
                    <Input
                        placeholder="Enter execution mode"
                        readOnly={!editMode}
                        style={{
                            backgroundColor: !editMode ? '#f5f5f5' : undefined,
                            cursor: !editMode ? 'not-allowed' : 'auto',
                        }}
                    />
                </Form.Item>

                <Form.Item label="Section URL" name="searchUri"
                    rules={[{ required: true, message: 'Please enter a URL' },
                    { type: 'url', warningOnly: true, message: 'Please enter a valid URL (e.g. https://example.com)', },
                    { type: 'string', min: 6 }]}
                >
                    <Input
                        placeholder="Enter "
                        readOnly={!editMode}
                        style={{
                            backgroundColor: !editMode ? '#f5f5f5' : undefined,
                            cursor: !editMode ? 'not-allowed' : 'auto',
                        }}
                    />
                </Form.Item>

                <Form.Item label="Active" name="isActive">
                    <Select
                        disabled={!editMode}
                        options={[
                            { label: 'Yes', value: 1 },
                            { label: 'No', value: 0 },
                        ]}
                        placeholder="Status required?"
                    />
                </Form.Item>

                <Form.Item
                    label="Priority"
                    name="priority"
                    rules={[{ type: 'number', min: 0, message: 'Must be a non-negative number' }]}
                >
                    <Input
                        type="number"
                        placeholder="Enter priority"
                        readOnly={!editMode}
                        style={{ backgroundColor: !editMode ? '#f5f5f5' : undefined, cursor: !editMode ? 'not-allowed' : 'auto' }}
                    />
                </Form.Item>

                <Form.Item
                    label="Section Rank"
                    name="sectionRank"
                    rules={[{ type: 'number', min: 0, message: 'Must be a non-negative number' }]}
                >
                    <Input
                        type="number"
                        placeholder="Enter section rank"
                        readOnly={!editMode}
                        style={{ backgroundColor: !editMode ? '#f5f5f5' : undefined, cursor: !editMode ? 'not-allowed' : 'auto' }}
                    />
                </Form.Item>

                <Form.Item
                    label="Max Days"
                    name="maxDays"
                    rules={[{ type: 'number', min: 0, message: 'Must be a non-negative number' }]}
                >
                    <Input
                        type="number"
                        placeholder="Enter max days"
                        readOnly={!editMode}
                        style={{ backgroundColor: !editMode ? '#f5f5f5' : undefined, cursor: !editMode ? 'not-allowed' : 'auto' }}
                    />
                </Form.Item>

                <Form.Item
                    label="Max Loops"
                    name="maxLoops"
                    rules={[{ type: 'number', min: 0, message: 'Must be a non-negative number' }]}
                >
                    <Input
                        type="number"
                        placeholder="Enter max loops"
                        readOnly={!editMode}
                        style={{ backgroundColor: !editMode ? '#f5f5f5' : undefined, cursor: !editMode ? 'not-allowed' : 'auto' }}
                    />
                </Form.Item>

                {editMode ? (
                    <Form.Item>
                        <Space>
                            <Button type="primary" onClick={handleSave}>
                                Save
                            </Button>
                            <Button onClick={handleCancel}>Cancel</Button>
                        </Space>
                    </Form.Item>
                ) : (
                    <Form.Item>
                        <Button onClick={() => setEditMode(true)}>Edit</Button>
                    </Form.Item>
                )}
            </Form>
        </>
    );
};

export default GeneralSetting;