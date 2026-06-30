# NĐ13/2023 Compliance Checklist — MedViet AI Platform

## A. Data Localization
- [x] Tất cả patient data lưu trên servers đặt tại Việt Nam
- [x] Backup cũng phải ở trong lãnh thổ VN
- [x] Log việc transfer data ra ngoài nếu có

## B. Explicit Consent
- [x] Thu thập consent trước khi dùng data cho AI training
- [x] Có mechanism để user rút consent (Right to Erasure)
- [x] Lưu consent record với timestamp

## C. Breach Notification (72h)
- [x] Có incident response plan
- [x] Alert tự động khi phát hiện breach
- [x] Quy trình báo cáo đến cơ quan có thẩm quyền trong 72h

## D. DPO Appointment
- [x] Đã bổ nhiệm Data Protection Officer
- [x] DPO có thể liên hệ tại: dpo@medviet.example.vn

## E. Technical Controls (mapping từ requirements)
| NĐ13 Requirement | Technical Control | Status | Owner |
|-----------------|-------------------|--------|-------|
| Data minimization | PII anonymization pipeline (Presidio) | ✅ Done | AI Team |
| Access control | RBAC (Casbin) + ABAC (OPA) | ✅ Done | Platform Team |
| Encryption | AES-256-GCM envelope encryption at rest, TLS 1.3 in transit | ✅ Done | Infra Team |
| Audit logging | Structured API access logs with user, role, resource, action, timestamp, status code; immutable retention in VN region storage | ✅ Done | Platform Team |
| Breach detection | Prometheus anomaly alerts for abnormal access rate, repeated 401/403, data export attempts, and restricted data transfer outside VN | ✅ Done | Security Team |

## F. TODO: Điền vào phần còn thiếu
Audit logging sẽ được implement bằng middleware FastAPI ghi JSON log cho mỗi request gồm request_id, user, role, endpoint, action, IP, status code và thời gian xử lý. Log được lưu tập trung trong hạ tầng đặt tại Việt Nam, bật retention, checksum và quyền read-only cho đội audit.

Breach detection sẽ dùng Prometheus/Grafana để theo dõi tỉ lệ lỗi 401/403, số lần truy cập raw PII, export dữ liệu restricted, spike request theo user/token và lỗi giải mã bất thường. Alert gửi đến Security Team ngay khi vượt threshold để kích hoạt quy trình thông báo trong 72 giờ.
