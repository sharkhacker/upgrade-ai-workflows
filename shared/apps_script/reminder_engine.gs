/**
 * Reminder Engine — Google Apps Script version.
 *
 * Production deployment target for the same logic the Python prototypes
 * demonstrate: bind this to the master tracker Google Sheet, add a daily
 * time-driven trigger on runDailyReminders(), and it scans the Filings,
 * DocumentsOut and Invoices tabs and emails reminders/escalations.
 *
 * Sheet layout mirrors data/*.csv in this repo (one tab per file,
 * header row = CSV header).
 */

var SECRETARY_EMAIL = 'company.secretary@firm.example.hk';
var ALERT_WINDOW_DAYS = 30;
var CHASE_THRESHOLDS = [7, 14, 21]; // gentle / firm / escalate

function runDailyReminders() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  checkFilingDeadlines_(ss.getSheetByName('Filings'));
  chaseUnsignedDocuments_(ss.getSheetByName('DocumentsOut'));
  chaseOverdueInvoices_(ss.getSheetByName('Invoices'));
}

function checkFilingDeadlines_(sheet) {
  eachRow_(sheet, function (row) {
    if (row.status !== 'pending' && row.status !== 'payment_due') return;
    var days = daysUntil_(row.due_date);
    if (days <= ALERT_WINDOW_DAYS) {
      var urgency = days < 0 ? 'OVERDUE' : days <= 7 ? 'URGENT' : 'Upcoming';
      MailApp.sendEmail(
        SECRETARY_EMAIL,
        '[' + urgency + '] ' + row.filing_type + ' for ' + row.company_id +
          ' due ' + row.due_date,
        row.description + '\nDays remaining: ' + days +
          '\nAction: notify client / confirm engagement.'
      );
    }
  });
}

function chaseUnsignedDocuments_(sheet) {
  eachRow_(sheet, function (row) {
    if (row.status !== 'awaiting_signature') return;
    var waiting = -daysUntil_(row.sent_date);
    var stage = stageFor_(waiting);
    if (stage === 0) return;
    var subject = 'Reminder ' + stage + ': unsigned "' + row.doc_type +
      '" (' + row.company_id + ', ' + waiting + ' days)';
    // Stage 1-2 chase the client; stage 3 also escalates internally.
    MailApp.sendEmail(SECRETARY_EMAIL, subject,
      'Draft chaser generated — review the AI draft in the outputs folder ' +
      'and send via the client\'s preferred channel.');
  });
}

function chaseOverdueInvoices_(sheet) {
  eachRow_(sheet, function (row) {
    if (row.status === 'paid' || row.status === 'draft') return;
    var overdue = -daysUntil_(row.due_date);
    if (overdue <= 0) return;
    MailApp.sendEmail(SECRETARY_EMAIL,
      'Invoice ' + row.invoice_no + ' is ' + overdue + ' days overdue (HKD ' +
        row.amount_hkd + ')',
      'Dunning stage: ' + stageFor_(overdue) + '. Review AI draft before sending.');
  });
}

// --- helpers ---------------------------------------------------------------

function eachRow_(sheet, fn) {
  var values = sheet.getDataRange().getValues();
  var header = values[0];
  for (var i = 1; i < values.length; i++) {
    var row = {};
    header.forEach(function (h, j) { row[h] = String(values[i][j]); });
    fn(row);
  }
}

function daysUntil_(dateStr) {
  var d = new Date(dateStr);
  return Math.floor((d - new Date()) / 86400000);
}

function stageFor_(daysWaiting) {
  var stage = 0;
  CHASE_THRESHOLDS.forEach(function (t, i) {
    if (daysWaiting >= t) stage = i + 1;
  });
  return stage;
}
