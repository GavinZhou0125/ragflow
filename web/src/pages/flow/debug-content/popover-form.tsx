import { useParseDocument } from '@/hooks/document-hooks';
import { useResetFormOnCloseModal } from '@/hooks/logic-hooks';
import { IModalProps } from '@/interfaces/common';
import { Button, Form, Input, Popover } from 'antd';
import { PropsWithChildren } from 'react';
import { useTranslation } from 'react-i18next';

const reg =
  /^(((ht|f)tps?):\/\/)?([^!@#$%^&*?.\s-]([^!@#$%^&*?.\s]{0,63}[^!@#$%^&*?.\s])?\.)+[a-z]{2,6}\/?/;

export const PopoverForm = ({
  children,
  visible,
  switchVisible,
  noValidateUrl,
  noOutputUrl,
}: PropsWithChildren<
  IModalProps<any> & { noValidateUrl?: boolean; noOutputUrl?: boolean }
>) => {
  const [form] = Form.useForm();
  const { parseDocument, loading } = useParseDocument();
  const { t } = useTranslation();

  useResetFormOnCloseModal({
    form,
    visible,
  });

  const onOk = async () => {
    const values = await form.validateFields();
    const val = values.url;

    if (reg.test(val)) {
      const ret = await parseDocument(val);
      if (ret?.data?.code === 0) {
        form.setFieldValue('result', ret?.data?.data);
        form.submit();

        if (noOutputUrl) {
          form.setFieldValue('url', '');
        }
      }
    }
  };

  const content = (
    <Form form={form} name="urlForm">
      <Form.Item
        name="url"
        rules={
          noValidateUrl
            ? [{ required: true }]
            : [{ required: true, type: 'url' }]
        }
        className="m-0"
      >
        <Input
          onPressEnter={(e) => e.preventDefault()}
          placeholder={t('flow.pasteFileLink')}
          suffix={
            <Button
              type="primary"
              onClick={onOk}
              size={'small'}
              loading={loading}
            >
              {t('common.submit')}
            </Button>
          }
        />
      </Form.Item>
      <Form.Item name={'result'} noStyle />
    </Form>
  );

  return (
    <Popover
      content={content}
      open={visible}
      trigger={'click'}
      onOpenChange={switchVisible}
    >
      {children}
    </Popover>
  );
};
